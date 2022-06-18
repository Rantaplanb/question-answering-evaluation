import pandas as pd
import sys, os
from functools import cmp_to_key
from fpdf import FPDF


def init_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('OpenSans', '', r"../../../resources/fonts/static/OpenSans/OpenSans-Regular.ttf")
    pdf.add_font('OpenSans', 'B', r"../../../resources/fonts/static/OpenSans/OpenSans-Bold.ttf")
    pdf.add_font('OpenSans', 'I', r"../../../resources/fonts/static/OpenSans/OpenSans-Italic.ttf")
    pdf.add_font('OpenSans', 'BI', r"../../../resources/fonts/static/OpenSans/OpenSans-BoldItalic.ttf")

    pdf.set_font('opensans', 'B', size=22)
    pdf.cell(w=190,txt='Model Evaluation', align='C')
    pdf.ln(25)
    return pdf


def select_input_file(input_dir_path):
    if '-input' in sys.argv:
        return sys.argv[sys.argv.index('-input') + 1]
    input_files = os.listdir(input_dir_path)
    print('The available input files are:')
    for i in range(len(input_files)):
        print(str(i + 1)  + ') ' + input_files[i])
    choice = input('Select input file number: ')
    if choice.isdigit() and int(choice) > 0 and int(choice) <= len(input_files):
        return input_files[int(choice ) - 1]
    else:
        print('Invalid input, expected number in range of (0 - ' + str(len(input_files)) + ')')
        print('Terminating ...')
        exit(0)


def compare_models(model1, model2):
    score1 = model1['yes'] + float(model1['partially']) / 2
    score2 = model2['yes'] + float(model2['partially']) / 2
    if score1 > score2:
        return -1
    elif score1 == score2:
        return 0
    else:
        return 1


def map_models_with_labels(models, labels):
    mapped_models = []
    for model in models: mapped_models.append({'model': model, 'yes': 0, 'partially': 0, 'no': 0})

    model_index = 0
    for label in labels:
        mapped_models[model_index][label] += 1

        if model_index == len(models) - 1:
            model_index = 0
        else:
            model_index += 1

    for model in mapped_models: model['total'] = model['yes'] + model['partially'] + model['no']

    mapped_models.sort(key=cmp_to_key(compare_models))
    return mapped_models


def get_input_data(input_filepath):
    data = pd.read_csv(input_filepath, encoding='UTF-16')
    return {
        "models": list(data['model'][:list(data['model'][1:]).index(data['model'][0]) + 1]), # Get models from csv,
        "labels": list(data['is_correct (labeled by machine)']),
        "questions": list(data['question']),
        "conf_scores": list(data['confidence_score'])
    }


def write_model_statistics_table(mapped_models, pdf):
    pdf.set_font('opensans', 'B', size=12)
    pdf.cell(txt='Model Statistics:', align='C')
    pdf.ln(6)

    headers = ['Model', 'Correct Answers', 'Partially Correct Answers', 'Wrong Answers']
    row = ['model', 'yes', 'partially', 'no']
    
    pdf.set_font('OpenSans', 'BI', size=8)
    for header in headers:
        pdf.multi_cell(60 if header == 'Model' else 42, 6, header, 1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.ln(6)

    
    for i in range(len(mapped_models)):
        for cell in row:
            if cell == 'model':
                pdf.set_font('OpenSans', 'BI', size=6)
                pdf.multi_cell(60, 10, mapped_models[i]['model'], 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
            else:
                pdf.set_font('OpenSans', 'I', size=6)
                pdf.multi_cell(42, 10, str(mapped_models[i][cell]) + ' (' + "{:2.1f}".format((mapped_models[i][cell] * 100) / mapped_models[i]['total']) + '%)', 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
        pdf.ln(10)
    pdf.ln(25)

def compare_resp_times(resp1, resp2):
    score1 = resp1['average'] 
    score2 = resp2['average'] 
    if score1 > score2:
        return 1
    elif score1 == score2:
        return 0
    else:
        return -1

def write_model_response_times(input_filename, models, pdf):
    input_dir = '../../1.BERT_models_QnA/output_data/'

    resp_times = list(pd.read_csv(input_dir + input_filename, encoding='UTF-16')['model_response_time'])
    
    model_resp_times = []
    for i in range(len(models)):
        model_resp_times.append([])

    for i in range(len(resp_times)):
        model_resp_times[i % len(models)].append(resp_times[i])

    model_time_stats = []
    for model in models: 
        model_time_stats.append({
            'model': model, 'average': 0, 'median': 0, 'min': 0, 'max': 0
        })


    for i in range(len(models)):
        model_resp_times[i].sort()
        model_time_stats[i]['average'] = sum(model_resp_times[i]) / len(model_resp_times[i])
        model_time_stats[i]['median'] = model_resp_times[i][int(len(model_resp_times[i]) / 2)]
        model_time_stats[i]['min'] = model_resp_times[i][0]
        model_time_stats[i]['max'] = model_resp_times[i][-1]

    model_time_stats.sort(key=cmp_to_key(compare_resp_times))
    
    pdf.set_font('opensans', 'B', size=12)
    pdf.cell(txt='Response Times Statistics:', align='C')
    pdf.ln(8)

    headers = ['Model', 'Average', 'Median', 'Min', 'Max']
    pdf.set_font('OpenSans', 'BI', size=8)
    for header in headers:
        pdf.multi_cell(60 if header == 'Model' else 31.5, 6, header, 1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.ln(6)

    row = ['model', 'average', 'median', 'min', 'max']
    for i in range(len(model_time_stats)):
        for cell in row:
            if cell == 'model':
                pdf.set_font('OpenSans', 'BI', size=6)
                pdf.multi_cell(60, 10, str(model_time_stats[i]['model']), 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
            else:
                pdf.set_font('OpenSans', 'I', size=6)
                pdf.multi_cell(31.5, 10, "{:2.1f}".format(model_time_stats[i][cell]), 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
        pdf.ln(10)
    pdf.ln(2)
    pdf.set_font('opensans', 'I', size=6)
    pdf.cell(txt='**All the response times are in seconds')
    pdf.ln(25)
    


def map_questions_with_labels(questions, labels, model_count):
    mapped_questions = []
    for question in questions: 
        if str(question) != 'nan':
            mapped_questions.append({'question': question, 'yes': 0, 'partially': 0 ,'no': 0, })
    
    question_index = 0
    models_passed = 0
    for label in labels:
        mapped_questions[question_index][label] += 1

        if models_passed == model_count - 1:
            models_passed = 0
            question_index += 1
        else:
            models_passed += 1

    return mapped_questions

def write_questions(questions, output_message, extra, pdf):
    pdf.set_font('opensans', 'B', size=8)
    pdf.cell(txt=str(len(questions)) + ' questions were answered ' + output_message, align='C')
    if extra == True:
        pdf.cell(txt=':')
        pdf.set_font('opensans', '', size=6)
        for question in questions:
            pdf.ln(4)
            pdf.cell(txt='  - ' + question)
        pdf.ln(6)
    else:
        pdf.ln(6)

def write_question_statistics(mapped_questions, extra_statistics, models, pdf):
    fully_correct = []
    fully_wrong = []
    at_least_one_correct = []
    exactly_one_correct = []
    correct_or_partially = []

    for question in mapped_questions:
        cur_question = question['question']
        if question['yes'] == len(models):
            fully_correct.append(cur_question)
        elif question['no'] == len(models):
            fully_wrong.append(cur_question)
        
        if question['yes'] > 0:
            at_least_one_correct.append(cur_question)
        if question['yes'] == 1:
            exactly_one_correct.append(cur_question)
        if question['no'] == 0:
            correct_or_partially.append(cur_question)
    
    pdf.set_font('opensans', 'B', size=12)
    pdf.cell(txt='Question Statistics:', align='C')
    pdf.ln(8)

    write_questions(fully_correct, 'correctly by all models', extra_statistics, pdf)
    write_questions(fully_wrong, 'incorrectly by all models', extra_statistics, pdf)
    write_questions(at_least_one_correct, 'correctly by at least one model', extra_statistics, pdf)
    write_questions(exactly_one_correct, 'correctly by exactly one model', extra_statistics, pdf)
    write_questions(correct_or_partially, 'correctly or partially correct by all models', extra_statistics, pdf)


def get_ranges(conf_scores):
    step = 0.1 
    j = 0
    results = []
    for i in range(10):
        counter = 0
        while(j < len(conf_scores) and step >= conf_scores[j]):
            j += 1
            counter += 1
        if len(conf_scores) == 0:
            results.append(['0', '0'])
        else:
            results.append([str(counter), '{:.1f}'.format(counter / len(conf_scores) * 100)])
        step += 0.1
    return results


def write_conf_score_graphs(conf_scores, models, labels, pdf):
    model_conf_scores = []

    for model in models: 
        model_conf_scores.append({'model': model, 'yes': [], 'partially': [], 'no': []})

    for i in range(len(labels)):
        model_conf_scores[i % len(models)][labels[i]].append(conf_scores[i])

    for dict in model_conf_scores:
        for arr in dict.values():
            if isinstance(arr, list):
                arr.sort()

    
    pdf.set_font('opensans', 'B', size=12)
    pdf.cell(txt='Model answers confidence scores:', align='C')
    pdf.ln(10)


    for i in range(len(models)):
        pdf.set_font('opensans', 'B', size=9)
        pdf.cell(txt='For ' + models[i] + ' model:', align='C')
        pdf.ln(6)
        headers = ['Range', 'Correct', 'Partially Correct', 'Wrong']
        pdf.set_font('OpenSans', 'BI', size=8)
        for header in headers:
            pdf.multi_cell(45, 6, header, 1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.ln(6)

        correct_ranges = get_ranges(model_conf_scores[i]['yes'])
        partially_ranges = get_ranges(model_conf_scores[i]['partially'])
        wrong_ranges = get_ranges(model_conf_scores[i]['no'])

        step = 0.1
        for row in range(10):
            for cell in range(4):
                if cell == 0:
                    pdf.set_font('OpenSans', 'BI', size=6)
                    pdf.multi_cell(45, 10, "{:2.1f}".format(step-0.1) + " - " + "{:2.1f}".format(step), 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
                elif cell == 1:
                    pdf.set_font('OpenSans', 'I', size=6)
                    pdf.multi_cell(45, 10, correct_ranges[row][0] + " (" + correct_ranges[row][1] + "%)", 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
                elif cell == 2:
                    pdf.set_font('OpenSans', 'I', size=6)
                    pdf.multi_cell(45, 10, partially_ranges[row][0] + " (" + partially_ranges[row][1] + "%)", 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
                else:
                    pdf.set_font('OpenSans', 'I', size=6)
                    pdf.multi_cell(45, 10, wrong_ranges[row][0] + " (" + wrong_ranges[row][1] + "%)", 1, align='C', new_x='RIGHT', new_y='TOP', max_line_height=120)
            pdf.ln(10)
            step += 0.1
        pdf.ln(10)
    pdf.ln(25)


if __name__ == '__main__':
    extra_statistics = True if '--extra' in sys.argv else False
    input_dir = '../../3.BERT_model_answer_labeling/output_data/'
    input_filename = select_input_file(input_dir)

    data = get_input_data(input_dir + input_filename)
    mapped_models = map_models_with_labels(data['models'], data['labels'])
    mapped_questions = map_questions_with_labels(data['questions'], data['labels'], len(data['models']))

    pdf = init_pdf()
    write_model_statistics_table(mapped_models, pdf)
    write_model_response_times(input_filename.replace('_auto_labeled', ''), data['models'], pdf)
    write_conf_score_graphs(data['conf_scores'], data['models'], data['labels'], pdf)
    write_question_statistics(mapped_questions, extra_statistics, data['models'], pdf)

    pdf.output('../output_data/statistics_for_' + input_filename[:-4]  + '.pdf')
