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


def scores_to_labels(scores, t1, t2):
    labels = []
    for score in scores:
        if float(score) > t1:
            labels.append('yes')
        elif float(score) > t2:
            labels.append('partially')
        else:
            labels.append('no')
    return labels


def write_data_to_csv(data, output_file):
    data.to_csv('../output_data/' + output_file, sep=',', encoding='UTF-16', index=False)

def select_thresholds():
    if '--thresholds' in sys.argv:
        t1 = float(sys.argv[sys.argv.index('-t1') + 1])
        t2 = float(sys.argv[sys.argv.index('-t2') + 1])
    else:
        t1 = float(input('\nEnter the first threshold number (if the total score of an answer is above the threshold, ' + \
                        'the answer will be labeled correct): '))
        t2 = float(input('Enter the second threshold number (if the total score of an answer is above the threshold, ' +\
                        'the answer will be labeled partially correct, the rest will be labeled wrong): '))
    if t2 > t1 or t1 > 1 or t2 < 0:
        print('Invalid thresholds given. Thresholds must be in the range [0, 1] and the 1st threshold must be bigger than the 2nd.')
        exit(1)
    return [t1, t2]


if __name__ == '__main__':
    input_dir = '../../2.BERT_model_answers_evaluation/output_data/'
    input_filename = select_input_file(input_dir)
    output_filename = input_filename.replace('evaluated_answers', 'QnA').replace('.csv', '_auto_labeled.csv')

    data = get_input_data(input_dir + input_filename)
    thresholds = select_thresholds()
    labels = scores_to_labels(data['sentence_transformer_score'], thresholds[0], thresholds[1])
    data['is_correct (labeled by machine)'] = labels

    write_data_to_csv(data, output_filename)