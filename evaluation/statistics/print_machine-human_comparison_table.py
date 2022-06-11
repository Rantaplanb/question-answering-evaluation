import pandas as pd

def get_labeled_answers(filename):
        dir_name = '../3.BERT_model_answer_labeling/output_data/'
        input_data = pd.read_csv(dir_name + filename + '.csv', encoding='UTF-16')
        return input_data['is_correct (labeled by machine)'], input_data['is_correct (labeled by human)']


def get_total_answers(human_labeled_dict):
    return human_labeled_dict['yes'] + human_labeled_dict['partially'] + human_labeled_dict['no']


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

if __name__ == "__main__":
    filename = 'QnA_on_custom_dataset_with_bing_fully_labeled'
    labeled_by_machine, labeled_by_human = get_labeled_answers(filename)

    row_entries = create_table_entries(labeled_by_machine, labeled_by_human)

    print_result_table(row_entries[0], \
                       row_entries[1], \
                       row_entries[2])