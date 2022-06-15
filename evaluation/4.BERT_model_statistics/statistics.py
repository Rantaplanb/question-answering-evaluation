import pandas as pd
import sys, os
from functools import cmp_to_key
from fpdf import FPDF


def init_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('OpenSans', '', r"../../resources/fonts/static/OpenSans/OpenSans-Medium.ttf")
    pdf.add_font('OpenSans', 'B', r"../../resources/fonts/static/OpenSans/OpenSans-Bold.ttf")
    pdf.add_font('OpenSans', 'I', r"../../resources/fonts/static/OpenSans/OpenSans-Italic.ttf")
    pdf.add_font('OpenSans', 'BI', r"../../resources/fonts/static/OpenSans/OpenSans-BoldItalic.ttf")

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
        "questions": list(data['question'])
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


def write_question_statistics(mapped_questions):
    fully_correct = []
    fully_wrong = []
    at_least_one_correct = []
    exactly_one_correct = []
    correct_or_partially = []

    for question in mapped_questions:
        cur_question = question['question']
        if question['yes'] == 10:
            fully_correct.append(cur_question)
        elif question['no'] == 10:
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

    pdf.set_font('opensans', 'B', size=8)
    pdf.cell(txt=str(len(fully_correct)) + ' questions were answered completely correct:', align='C')
    pdf.set_font('opensans', '', size=6)
    for question in fully_correct:
        pdf.ln(4)
        pdf.cell(txt='  - ' + question)




if __name__ == '__main__':
    input_dir = '../3.BERT_model_answer_labeling/output_data/'
    input_filename = select_input_file(input_dir)
    
    data = get_input_data(input_dir + input_filename)
    mapped_models = map_models_with_labels(data['models'], data['labels'])
    mapped_questions = map_questions_with_labels(data['questions'], data['labels'], len(data['models']))

    pdf = init_pdf()
    write_model_statistics_table(mapped_models, pdf)
    write_question_statistics(mapped_questions)

    pdf.output('statistics.pdf')
