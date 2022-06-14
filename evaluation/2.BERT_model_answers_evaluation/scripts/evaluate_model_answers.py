from cmath import nan
import spacy, csv, os, sys
import pandas as pd
import Levenshtein
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util


nlp = spacy.load("en_core_web_lg")
sentence_transformer = SentenceTransformer('distilbert-base-nli-mean-tokens')
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
        'models' : list(data['model'][:list(data['model'][1:]).index(data['model'][0]) + 1]), # Get models from csv
        'gr_correct_answers' : list(data['gr_correct_answer']),
        'gr_model_answers' : list(data['gr_model_answer']),
        'en_correct_answers' : list(data['en_correct_answer']),
        'en_model_answers' : list(data['en_model_answer']),
        'confidence_scores' : list(data['confidence_score'])
    }


def get_output_filename(input_filename):
    if 'custom' in input_filename:
        return 'evaluated_answers_on_custom_dataset_with_' + input_filename[input_filename.index('with_') + 5 : - 4] + '.csv'        
    elif 'xquad' in input_filename:
        return 'evaluated_answers_on_xquad_with_' + input_filename[input_filename.index('with_') + 5 : - 4] + '.csv'
    else:
        print("No man's land.")
        exit(0)


def format_answer(answer):
    return answer.lower().replace('.', '').replace(',', '').replace('\'', '')\
                 .replace('\"', '').replace('-', '').replace('%', '').replace(':', '')

def calc_nlp_score(correct_answer, model_answer):
    return float("{:.3f}".format(nlp(model_answer).similarity(nlp(correct_answer))))

def calc_levenshtein_score(correct_answer, model_answer):
    return float("{:.3f}".format(1 - (float(Levenshtein.distance(model_answer, correct_answer)) / (max(len(model_answer), len(correct_answer))))))

def calc_substring_score(correct_answer, model_answer):
    return float("{:.3f}".format(SequenceMatcher(None, model_answer, correct_answer).ratio()))

def calc_sentence_transformer_score(correct_answer, model_answer):
    sentence_embeddings = sentence_transformer.encode([model_answer, correct_answer])
    return float("{:.3f}".format(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])[0][0].item()))

def count_common_words(s0, s1):
    s0 = s0.lower()
    s1 = s1.lower()
    s0List = s0.split(" ")
    s1List = s1.split(" ")
    return len(list(set(s0List)&set(s1List)))

def calc_f1_score(correct_answer, model_answer):
    common_words_count = count_common_words(model_answer, correct_answer)
    precision = common_words_count / len(model_answer.split(" "))
    recall = common_words_count / len(correct_answer.split(" "))
    return 0 if precision == 0 and recall == 0 else float("{:.3f}".format((2 * precision * recall) / (precision + recall)))


def calculate_scores(correct_answers, model_answers, weights):
    scores = {'nlp': [], 'levenshtein': [], 'substring': [], 'sentence_transformers': [], 'f1': []}
    total_scores = []
    score_calculators = {
        'nlp': calc_nlp_score, 
        'levenshtein': calc_levenshtein_score, 
        'substring': calc_substring_score, 
        'sentence_transformers': calc_sentence_transformer_score, 
        'f1': calc_f1_score
        }

    for i in range(len(correct_answers)):
        total_score = 0
        correct_answer = format_answer(correct_answers[i])
        model_answer = format_answer(model_answers[i])

        if model_answer.isnumeric() and correct_answer.isnumeric():
            for score_list in scores.values():
                score_list.append('-')
            total_score = 1 if model_answer == correct_answer else 0
        else:
            for score, score_list in scores.items():
                cur_score = score_calculators[score](correct_answer, model_answer)
                total_score += cur_score * weights[score]
                score_list.append(cur_score)
        total_scores.append(total_score)
    
    scores['total'] = total_scores
    return scores

def check_weights(weights):
    total = 0
    for weight in weights.values():
        total += weight 
    if (1.0 - total) < -0.0001 or (1.0 - total) > 0.0001:
        print('Incorrect sum of weights...')
        return False
    return True


def select_weights():
    if '--weights' in sys.argv:
        weights =  {
            'nlp': float(sys.argv[sys.argv.index('-nlp') + 1]),
            'levenshtein': float(sys.argv[sys.argv.index('-levenshtein') + 1]),
            'substring': float(sys.argv[sys.argv.index('-substring') + 1]),
            'sentence_transformers': float(sys.argv[sys.argv.index('-sentence_trans') + 1]),
            'f1': float(sys.argv[sys.argv.index('-f1') + 1])
        }
    else:
        weights = {'nlp': 0.2, 'levenshtein': 0.1, 'substring': 0.1, 'sentence_transformers': 0.4, 'f1': 0.2}
        print('\nTo select a weight for each string comparison metric, enter a number in the range [0, 1].')
        print('The sum of all given weights, must be equal to 1.')
        print('If you want to use the default weights, press enter.\n')
        for metric in weights.keys():
            if metric == 'nlp':
                user_input = input('NLP weight: ')
            else:
                user_input = input(metric.capitalize() + ' weight: ')
            if user_input == '':
                print('Default weights were set!')
                break
            else:
                weights[metric] = float(user_input)

    return weights if check_weights(weights) else exit(1)


def write_headers(filename, headers):
    with open('../output_data/' + filename, 'w', encoding='UTF16') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def write_scores(data, scores, filename):
    headers = ['question', 'model', 'gr_correct_answer', 'gr_model_answer', 'en_correct_answer', 
               'en_model_answer', 'confidence_score', 'nlp_score', 'levenshtein_score', 
               'substring_score', 'sentence_transformer_score', 'f1_score', 'total_score']
    write_headers(filename, headers)
               
    with open('../output_data/' + filename, 'a', encoding='UTF16') as file:
        writer = csv.writer(file)
        for i in range(len(scores['total'])):
            writer.writerow([
                '' if str(data['questions'][i]) == 'nan' else data['questions'][i], 
                data['models'][i % len(data['models'])],
                data['gr_correct_answers'][i],
                data['gr_model_answers'][i],
                data['en_correct_answers'][i],
                data['en_model_answers'][i],
                data['confidence_scores'][i],
                scores['nlp'][i],
                scores['levenshtein'][i],
                scores['substring'][i],
                scores['sentence_transformers'][i],
                scores['f1'][i],
                scores['total'][i]
            ])


if __name__ == "__main__":
    input_dir = '../../1.BERT_models_QnA/output_data/'
    input_filename = select_input_file(input_dir)

    data = get_QnA_results(input_dir + input_filename)
    weights = select_weights()
    scores = calculate_scores(data['en_correct_answers'], data['en_model_answers'], weights)

    output_filename = get_output_filename(input_filename)
    write_scores(data, scores, output_filename)