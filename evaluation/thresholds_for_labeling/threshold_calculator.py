import os, sys
import pandas as pd


def select_input_file(input_dir_path):
    if len(sys.argv) != 2:
        print('The script must be executed with exactly one file as command line argument.')
        print('Terminating ...')
        exit(-1)
    return sys.argv[1]

def get_input_data(input_filepath):
    data = pd.read_csv(input_filepath, encoding='UTF-16')
    return list(data['is_correct (labeled by human)'])

def get_total_answers(dicts):
    total = 0
    for dict in dicts:
        total += dict['yes']
        total += dict['partially']
        total += dict['no']
    return total

def create_table_entries(labeled_by_machine, labeled_by_human):
    human_labeled_correct_dict = {'yes' : 0, 'partially' : 0, 'no' : 0}
    human_labeled_partially_dict = {'yes' : 0, 'partially' : 0, 'no' : 0}
    human_labeled_wrong_dict = {'yes' : 0, 'partially' : 0, 'no' : 0}  

    for index in range(len(labeled_by_machine)):
        human_label = labeled_by_human[index]
        machine_label = labeled_by_machine[index]
        if human_label == 'invalid':
            continue
        elif human_label == 'yes':
            human_labeled_correct_dict[machine_label] += 1
        elif human_label == 'partially':
            human_labeled_partially_dict[machine_label] += 1
        elif human_label == 'no':
            human_labeled_wrong_dict[machine_label] += 1

    return [human_labeled_correct_dict, human_labeled_partially_dict, human_labeled_wrong_dict]

def get_threshold_score(dicts):
    return dicts[0]['yes'] + dicts[1]['partially'] + dicts[2]['no'] / get_total_answers(dicts)

def get_new_machine_labels(input_filename, t1, t2):
    os.system(
        'cd ../3.BERT_model_answer_labeling/scripts;' + 
        'python label_model_answers.py -input ' + input_filename + ' --thresholds -t1 ' + str(t1) + ' -t2 ' + str(t2) + ';'
    )
    data = pd.read_csv('../3.BERT_model_answer_labeling/output_data/' + input_filename.replace('evaluated_answers', 'QnA').replace('.csv', '_auto_labeled.csv'), encoding='utf16')
    return data['is_correct (labeled by machine)']

def find_best_thresholds(threshold_scores):
    max_item = threshold_scores[0]
    for item in threshold_scores:
        if item['score'] > max_item['score']:
            max_item = item
    return max_item['t1'], max_item['t2']

def calculate_thresholds(human_labels, filename_step2):
    threshold_scores = []
    step = 0.01
    t1 = 0.00
    t2 = 0.0
    while t2 < 1:
        while t1 < 1:
            if t1 > t2:
                machine_labels = get_new_machine_labels(filename_step2, t1, t2)
                score = get_threshold_score(create_table_entries(machine_labels, human_labels))
                print('Appending' + score)
                threshold_scores.append({'t1': t1, 't2': t2, 'score': score})
            t1 += step
        t1 = 0
        t2 += step
    return find_best_thresholds(threshold_scores)


def print_result_table(correct_dict, partially_dict, wrong_dict):
    print('---------------------------------------------------------------------------------------------------------------------')
    print('{:<25}  {:<25}  {:<25}  {:<25}  {:<7}'\
        .format('| Human Labeling', 'Machine Labeled Yes', 'Machine Labeled Partially', 'Machine Labeled No', 'Total'), '|')
    print('|-------------------------------------------------------------------------------------------------------------------|')
    print('{:<25}  {:<25}  {:<25}  {:<25}  {:<7}'\
        .format('| Yes', correct_dict['yes'], correct_dict['partially'], correct_dict['no'], get_total_answers(correct_dict)), '|')
    print('{:<25}  {:<25}  {:<25}  {:<25}  {:<7}'\
        .format('| Partially', partially_dict['yes'], partially_dict['partially'], partially_dict['no'], get_total_answers(partially_dict)), '|')
    print('{:<25}  {:<25}  {:<25}  {:<25}  {:<7}'\
        .format('| No', wrong_dict['yes'], wrong_dict['partially'], wrong_dict['no'], get_total_answers(wrong_dict)), '|')
    print('---------------------------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    input_dir = './QnA_fully_labeled/'
    input_filename = select_input_file(input_dir)
    filename_step2 = input_filename.replace('QnA', 'evaluated_answers').replace('_fully_labeled', '')
    human_labels = get_input_data(input_dir + input_filename)

    t1, t2 = calculate_thresholds(human_labels, filename_step2)

    print('Final thresholds: ', t1, t2)