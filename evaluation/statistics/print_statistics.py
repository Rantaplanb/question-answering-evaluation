import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from functools import cmp_to_key
import statistics

our_context_count = 20
xsquad_context_count = 118
xsquad_context_count_bing = 45

translator = 'helsinki'
total_contexts = our_context_count
questions_per_context = 10
model_count = 10

def get_data(translator):
    return pd.read_csv('../../resources/csv_files/questions_with_answers_from_all_models_on_our_collection_' + translator + '.csv', encoding='utf16')
    # return pd.read_csv('../../resources/csv_files/questions_with_answers_from_all_models_on_xsquad_bing_with_is_correct.csv', encoding='utf16')

data = get_data(translator)
is_correct_col = data['is_correct']
questions_col = data['question']
scores_col = data['score']
models_col = data['model']

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
    is_correct = []
    for i in range(total_contexts * questions_per_context):
        current_index = (i * questions_per_context) + model_index
        if is_correct_col[current_index] == 'invalid':
            continue
        scores.append(scores_col[current_index])
        is_correct.append(is_correct_col[current_index])

    return scores, is_correct

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
    exactly_one_correct_models = []
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

    # Finding the models that answered correct in a question while the others answered wrong.
    exactly_one_correct_models = {models[0]:0, models[1]:0, models[2]:0, models[3]:0, models[4]:0, models[5]:0, models[6]:0, models[7]:0, models[8]:0, models[9]:0}
    for question in exactly_one_correct:
        starting_index = list(questions_col).index(question)
        for i in range(questions_per_context):
            if is_correct_col[starting_index + i] == 'yes':
                exactly_one_correct_models[models_col[starting_index + i]] += 1

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
    print('\033[01;31m','\n------------------------------------------------------------','\033[00m', sep='')
    print_yellow()
    print('Models that answered a question correctly while the other failed: ')
    print('\033[01;31m','------------------------------------------------------------','\033[00m', sep='')
    for m in exactly_one_correct_models:
        if exactly_one_correct_models[m] != 0:
            print(m, "->", exactly_one_correct_models[m], "times" )
    
def convert_evaluation_to_num(table):
    temp_table = []
    for item in table:
        if item == 'yes':
            temp_table.append(1)
        elif item == 'no':
            temp_table.append(0)
        else:
            temp_table.append(0.5)

    return temp_table

def plot_confidence_score_with_evaluation(model):
    model_index = models.index(model)

    scores, is_correct = get_model_scores(model)
    
    plt.scatter((is_correct), scores)
    plt.title(model)
    plt.xlabel("Is Correct")
    plt.ylabel("Confidence Score")
    plt.show()

def print_ranges(conf_scores, answer):
    step = 0.1 
    j = 0
    percentage_counter = 0
    for i in range(10):
        counter = 0
        while(j < len(conf_scores) and step >= conf_scores[j]):
            j += 1
            counter += 1
        percentage_counter += counter
        print('In confidence range [', "{:.1f}".format(step - 0.1) , '-', "{:.1f}".format(step), ']:', counter , answer, 'answers', '{:.1f}'.format(counter / len(conf_scores) * 100), '%', '\t| Total Percantage so far' , '{:.1f}'.format(percentage_counter / len(conf_scores) * 100), '%')
        step += 0.1
    print('-------------------------------------------------------------------------------------------------')

def print_confidence_statistics(model):
    scores, is_correct = get_model_scores(model)

    correct_answers_conf_scores = []
    wrong_answers_conf_scores = []
    partially_correct_answers_conf_scores = []
    for i in range(len(is_correct)):
        if is_correct[i] == 'yes':
            correct_answers_conf_scores.append(scores[i])
        elif is_correct[i] == 'no':
            wrong_answers_conf_scores.append(scores[i])
        elif is_correct[i] == 'partially':
            partially_correct_answers_conf_scores.append(scores[i])

    correct_answers_conf_scores.sort()
    wrong_answers_conf_scores.sort()
    partially_correct_answers_conf_scores.sort()

    print('For ', model, ':')
    print('-------------------------------------------------------------------------------------------------')
    print('For correct answers:{ Average: ', "{:.3f}".format(sum(correct_answers_conf_scores) / len(correct_answers_conf_scores)), ', Median: ', "{:.3f}".format(statistics.median(correct_answers_conf_scores)), '}', sep='')
    print('For wrong answers:{ Average: ', "{:.3f}".format(sum(wrong_answers_conf_scores) / len(wrong_answers_conf_scores)), ', Median: ', "{:.3f}".format(statistics.median(wrong_answers_conf_scores)), '}', sep='')
    print('For partially correct answers:{ Average: ', "{:.3f}".format(sum(partially_correct_answers_conf_scores) / len(partially_correct_answers_conf_scores)), ', Median: ', "{:.3f}".format(statistics.median(partially_correct_answers_conf_scores)), '}', sep='')
    print('-------------------------------------------------------------------------------------------------')
    print_ranges(correct_answers_conf_scores, 'correct')
    print_ranges(wrong_answers_conf_scores, 'wrong')
    print_ranges(partially_correct_answers_conf_scores, 'partially correct')

    


if __name__ == "__main__":
    model_results = []
    for i in range(model_count):
        model_results.append(get_model_results(models[i]))
    invalid_count = model_results[-1]['invalid'] * 10
    print_model_statistics(model_results)

    question_results = []
    for i in range(total_contexts):
        for j in range(questions_per_context):
            question_results.append(get_question_results(i, j))
    print_question_statistics(question_results)

    for model in models:
        print_confidence_statistics(model)
        #plot_confidence_score_with_evaluation(model)
        print()
        print()
        print()
