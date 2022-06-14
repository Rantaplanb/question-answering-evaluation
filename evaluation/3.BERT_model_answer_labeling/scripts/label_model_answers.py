import pandas as pd
import re

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


def write_model_answer_labels(data, output_file):
    total_scores = data['total_score']
    is_correct = []
    for total_score in total_scores:
        if float(total_score) > 0.65:
            is_correct.append('yes')
        elif float(total_score) > 0.5:
            is_correct.append('partially')
        else:
            is_correct.append('no')
    data['is_correct (labeled by machine)'] = is_correct
    data.to_csv('../output_data/' + output_file, sep=',', encoding='UTF-16', index=False)


if __name__ == '__main__':
    input_dir = '../../2.BERT_model_answers_evaluation/output_data/'
    input_filename = select_input_file(input_dir)

    data = get_input_data(input_dir + input_filename)

    output_filename = ''
    if 'custom' in input_filename:
        if 'bing' in input_filename:
            output_filename = 'QnA_on_custom_dataset_with_bing_fully_labeled.csv'
        elif 'helsinki' in input_filename:
            output_filename = 'QnA_on_custom_dataset_with_helsinki_fully_labeled.csv'
        else:
            #TODO: Ti kanoume me to multilingual???
            pass
    elif 'xquad' in input_filename:
        if 'bing' in input_filename:
            output_filename = 'QnA_on_xquad_with_bing_auto_labeled.csv'
        elif 'helsinki' in input_filename:
            output_filename = 'QnA_on_xquad_with_helsinki_auto_labeled.csv'
        else:
            #TODO: Ti kanoume me to multilingual???
            pass
    else:
        print('no mans land')

    write_model_answer_labels(data, output_filename)