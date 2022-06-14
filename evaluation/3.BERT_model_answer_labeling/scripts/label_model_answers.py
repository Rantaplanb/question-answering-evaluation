import pandas as pd
import sys, os

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


def get_input_data(input_filepath):
    return pd.read_csv(input_filepath, encoding='UTF-16')


def scores_to_labels(scores):
    labels = []
    for score in scores:
        if float(score) > 0.65:
            labels.append('yes')
        elif float(score) > 0.5:
            labels.append('partially')
        else:
            labels.append('no')
    return labels


def write_data_to_csv(data, output_file):
    data.to_csv('../output_data/' + output_file, sep=',', encoding='UTF-16', index=False)


if __name__ == '__main__':
    input_dir = '../../2.BERT_model_answers_evaluation/output_data/'
    input_filename = select_input_file(input_dir)
    output_filename = input_filename.replace('evaluated_answers', 'QnA').replace('.csv', '_auto_labeled.csv')

    data = get_input_data(input_dir + input_filename)

    labels = scores_to_labels(data['total_score'])
    data['is_correct (labeled by machine)'] = labels
    write_data_to_csv(data, output_filename)