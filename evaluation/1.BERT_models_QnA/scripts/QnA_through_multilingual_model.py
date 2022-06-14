import csv, json, os, sys
from transformers import pipeline
import time

def answer_question(context, question, model):
    start = time.time()
    question_answerer = pipeline(task="question-answering", model = model)
    answer = question_answerer(question = question, context = context)
    end = time.time()
    return answer, end-start


def get_dataset(filename):
    if filename == 'custom_QnA_dataset.json':
        f = open('../../../resources/json_files/' + filename, encoding='UTF16')
        return json.load(f)["collection"]
    elif filename == 'squad_QnA_dataset.json':
        f = open('../../../resources/json_files/' + filename, encoding='UTF8')
        return json.load(f)["data"]


def write_headers(filename, headers):
    with open('../output_data/' + filename, 'w', encoding='UTF16') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def QnA_on_custom_dataset(dataset, output_file, model):
    headers = ['question', 'correct_answer', 'model_answer', 'model_response_time', 'confidence_score']
    write_headers(output_file, headers)
    for set in dataset:
        context = set['context']
        questions = set['questions']
        answers = set['answers']

        print('Context: ', context)
        for i in range(len(questions)):
            question = questions[i]
            print('Question: ', question)
            result, elapsed_time = answer_question(context, question, model)
            result_row = [question, answers[i], result['answer'], elapsed_time, result['score']]
            question = ""
            with open('../output_data/' + output_file, 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                writer.writerow(result_row)


def QnA_on_xquad(dataset, output_file, model):
    headers = ['question', 'correct_answer', 'model_answer', 'model_response_time', 'confidence_score']
    write_headers(output_file, headers)

    for subject in dataset:
        paragraphs = subject["paragraphs"]
        for QnA in paragraphs:
            context = QnA['context']
            print('Context: ', context)
            for qna in QnA["qas"]:
                question = qna["question"]
                print('Question: ', question)
                result, elapsed_time = answer_question(context, question, model)
                result_row = [question, qna['answers'][0]['text'], result['answer'], elapsed_time, result['score']]
                question = ""
                with open('../output_data/' + output_file, 'a', encoding='UTF16') as file:
                    writer = csv.writer(file)
                    writer.writerow(result_row)


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

"""
---Script Configuration---
- To select a different multilingual QnA BERT model:
  In function main, change the value of the model variable
  to the name of your multilingual model of choice.
- To add your own input QnA dataset:
    1) Add your own json file to the ${PROJECT_ROOT}/resources/json_files/ directory.
    2) Modify get_dataset() to load your json file.
    3) Implement your own QnA_on_${DATASET_NAME} function using answer_question(). 
    4) Add a case in main() for your json dataset and call your function implemented in (3).
"""
if __name__ == '__main__':
    model = "deepset/xlm-roberta-large-squad2"
    input_dir = '../../../resources/json_files/'
    input_filename = select_input_file(input_dir)

    dataset = get_dataset(input_filename)

    if input_filename == 'custom_QnA_dataset.json':
        output_filename = 'QnA_on_custom_dataset_with_' + model.replace('/', '-') + '.csv'
        QnA_on_custom_dataset(dataset, output_filename, model)
    elif input_filename == 'squad_QnA_dataset.json':
        output_filename = 'QnA_on_xquad_with_' + model.replace('/', '-') + '.csv'
        QnA_on_xquad(dataset, output_filename, model)
    else:
        print("No man's land.")