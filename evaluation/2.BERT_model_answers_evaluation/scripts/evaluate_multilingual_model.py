import csv, re, os, sys
import pandas as pd
from sentence_transformers import SentenceTransformer, util

sentence_transformer_multilingual = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased')


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


def get_QnA_results(filepath):
    data = pd.read_csv(filepath, encoding='UTF-16')
    return {
        'questions' : list(data['question']),
        'correct_answers' : list(data['correct_answer']),
        'model_answers' : list(data['model_answer']),
        'confidence_scores' : list(data['confidence_score'])
    }


def format_answer(answer):
    return answer.lower().replace('.', '').replace(',', '').replace('\'', '')\
                 .replace('\"', '').replace('-', '').replace('%', '').replace(':', '')


def calc_multilingual_sentence_transformer_score(correct_answer, model_answer):
    sentence_embeddings = sentence_transformer_multilingual.encode([model_answer, correct_answer])
    return float("{:.3f}".format(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])[0][0].item()))


def calculate_scores(correct_answers, model_answers):
    multilingual_sentence_transformer_scores = []
    for i in range(len(correct_answers)):
        total_score = 0
        correct_answer = format_answer(correct_answers[i])
        model_answer = format_answer(model_answers[i])

        if model_answer.isnumeric() and correct_answer.isnumeric():
            for score_list in scores.values():
                score_list.append('-')
            total_score = 1 if model_answer == correct_answer else 0
        else:
            multilingual_sentence_transformer_scores\
                .append(calc_multilingual_sentence_transformer_score(correct_answer, model_answer))
    
    return multilingual_sentence_transformer_scores


def get_output_filename(input_filename):
    if 'custom' in input_filename:
        return 'evaluated_answers_on_custom_dataset_with_' + input_filename[input_filename.index('with_') + 5 : - 4] + '.csv'        
    elif 'xquad' in input_filename:
        return 'evaluated_answers_on_xquad_with_' + input_filename[input_filename.index('with_') + 5 : - 4] + '.csv'
    else:
        print("No man's land.")
        exit(0)


def write_headers(filename, headers):
    with open('../output_data/' + filename, 'w', encoding='UTF16') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

def write_scores(data, scores, filename):
    headers = ['question', 'correct_answer', 'model_answer', 
            'confidence_score', 'sentence_transformer_score']
    write_headers(filename, headers)
               
    with open('../output_data/' + filename, 'a', encoding='UTF16') as file:
        writer = csv.writer(file)
        for i in range(len(scores)):
            writer.writerow([
                '' if str(data['questions'][i]) == 'nan' else data['questions'][i], 
                data['correct_answers'][i],
                data['model_answers'][i],
                data['confidence_scores'][i],
                scores[i],
            ])


if __name__ == "__main__":
    input_dir = '../../1.BERT_models_QnA/output_data/'
    input_filename = select_input_file(input_dir)

    data = get_QnA_results(input_dir + input_filename)
    scores = calculate_scores(data['correct_answers'], data['model_answers'])

    output_filename = get_output_filename(input_filename)
    write_scores(data, scores, output_filename)