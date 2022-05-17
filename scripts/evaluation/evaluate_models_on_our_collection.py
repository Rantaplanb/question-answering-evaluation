import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from functools import cmp_to_key

translator = 'bing'
total_contexts = 20
questions_per_context = 10
model_count = 10

def get_data(translator):
    return pd.read_csv('../../resources/csv_files/questions_with_answers_from_all_models_on_our_collection_' + translator + '.csv', encoding='utf16')

data = get_data(translator)
is_correct_col = data['is_correct']
questions_col = data['question']
scores_col = data['score']

models = [
    "deepset/roberta-base-squad2",
    "bert-large-uncased-whole-word-masking-finetuned-squad",
    "distilbert-base-cased-distilled-squad",
    "deepset/bert-large-uncased-whole-word-masking-squad2",
    "distilbert-base-uncased-distilled-squad",
    "rsvp-ai/bertserini-bert-base-squad",
    "deepset/minilm-uncased-squad2",
    "dmis-lab/biobert-large-cased-v1.1-squad",
    "deepset/bert-base-cased-squad2",
    "bert-large-cased-whole-word-masking-finetuned-squad"]

def get_model_results(model):
    results = {'model': model, 'translator': translator, 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }
    model_index = models.index(model)

    for i in range(total_contexts * questions_per_context):
        current_index = (i * questions_per_context) + model_index
        results[is_correct_col[current_index]] += 1
    return results


def get_question_results(context_index, question_index):
    starting_index = (context_index * model_count * questions_per_context) + (question_index * questions_per_context)
    results = {'question': questions_col[starting_index], 'translator': translator, 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }
    for i in range(questions_per_context):
        results[is_correct_col[starting_index + i]] += 1
    return results


def get_model_scores(model):
    model_index = models.index(model)
    scores = []
    for i in range(total_contexts * questions_per_context):
        current_index = (i * questions_per_context) + model_index
        scores.append(scores_col[current_index])
    return scores

def compare_model_results(res1, res2):
    score1 = res1['yes'] + float(res1['partially']) / 2
    score2 = res2['yes'] + float(res2['partially']) / 2
    if score1 > score2:
        return 1
    elif score1 == score2:
        return 0
    else:
        return -1

def print_model_statistics(model_results):
    model_results.sort(key=cmp_to_key(compare_model_results))
    
    for result in model_results:
        print('For model', result['model'], ':')
        print('Correct:', result['yes'])
        print('Partially correct:', result['partially'])
        print('Wrong:', result['no'])
        print('Percentage:', "{:.2f}".format((result['yes'] + float(result['partially'])/2) / (result['yes'] + result['partially'] + result['no'])*100), '%')
        print('---------------------------------------------------')

def compare_question_results(ques1, ques2):
    score1 = ques1['yes'] + float(ques1['partially']) / 2
    score2 = ques2['yes'] + float(ques2['partially']) / 2
    if score1 > score2:
        return 1
    elif score1 == score2:
        return 0
    else:
        return -1

def print_yellow():
    print('\033[01;33m', end='', sep='')

def reset_print_color():
    print('\033[01;37m', end='', sep='')

def print_question_statistics(question_results):
    question_results.sort(key=cmp_to_key(compare_question_results))

    invalid_questions = []
    fully_wrong_questions = []
    exactly_one_correct = []
    at_least_one_correct = []
    correct_or_partially = []
    fully_correct_questions = []
    for result in question_results:
        cur_question = result['question']
        if result['invalid'] == 10:
            invalid_questions.append(cur_question)
        elif result['yes'] == 10:
            fully_correct_questions.append(cur_question)
        elif result['no'] == 10:
            fully_wrong_questions.append(cur_question)
        
        if result['yes'] > 0:
            at_least_one_correct.append(cur_question)
        if result['yes'] == 1:
            exactly_one_correct.append(cur_question)
        if result['no'] == 0 and result['invalid'] == 0:
            correct_or_partially.append(cur_question)

    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(invalid_questions), ' questions were invalid due to incorrect translation: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')
    for q in invalid_questions:
        print(q)
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(fully_wrong_questions), 'questions were answered completely wrong: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')
    for q in fully_wrong_questions:
        print(q)
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(exactly_one_correct), 'questions were answered correctly by exactly one model: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')
    for q in exactly_one_correct:
        print(q)
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(at_least_one_correct), 'questions were answered correctly by at least one model: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')

    for q in at_least_one_correct:
        print(q)
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(correct_or_partially), 'questions had no wrong answers (only correct or partially correct): ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')

    for q in correct_or_partially:
        print(q)
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print(len(fully_correct_questions), 'questions were answered completely correct: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')

    for q in fully_correct_questions:
        print(q)
    

if __name__ == "__main__":
    model_results = []
    for i in range(model_count):
        model_results.append(get_model_results(models[i]))
    invalid_count = model_results[-1]['invalid'] * 10
    #print_model_statistics(invalid_count)

    question_results = []
    for i in range(total_contexts):
        for j in range(questions_per_context):
            question_results.append(get_question_results(i, j))
    print_question_statistics(question_results)
    
    # converted_bing_model_evaluation = convert_model_is_correct_column_to_num(bing_model_evaluation)

    # r = np.corrcoef(np.array(converted_bing_model_evaluation), np.array(bing_prediction_scores))
    # print(r)
    # plt.plot(converted_bing_model_evaluation, bing_prediction_scores)

    