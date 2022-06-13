from asyncore import write
import csv, json, time, threading, os, sys, inspect
from transformers import pipeline
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname( \
    os.path.abspath(inspect.getfile(inspect.currentframe()))))))
from utils.translator import translate

def answer_question(context, question, model):
    start = time.time()
    question_answerer = pipeline(task="question-answering", model = model)
    answer = question_answerer(question = question, context = context)
    end = time.time()
    return answer, end-start

def get_dataset(filename):
    if filename == 'custom_QnA_dataset.json':
        f = open('../../../resources/json_files/' + filename, encoding='utf-16')
        return json.load(f)["collection"]
    elif filename == 'squad_QnA_dataset.json':
        f = open('../../../resources/json_files/' + filename, encoding='UTF8')
        return json.load(f)["data"]


def write_headers(filename, headers):
    with open('../output_data/' + filename, 'w', encoding='UTF16') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def select_input_file(input_dir_path):
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

def select_translator():
    print('The available translators are:\n1) Bing\n2) Helsinki ')
    choice = input('Select translator number: ')
    if choice.isdigit() and int(choice) > 0 and int(choice) <= 2:
        return 'bing' if choice == 1 else 'helsinki'
    else:
        print('Invalid input, expected number in range of (0 - 2)')
        print('Terminating ...')
        exit(0)

def get_models():
    return [
    "deepset/roberta-base-squad2",
    "bert-large-uncased-whole-word-masking-finetuned-squad",
    "distilbert-base-cased-distilled-squad",
    "deepset/bert-large-uncased-whole-word-masking-squad2",
    "distilbert-base-uncased-distilled-squad",
    "rsvp-ai/bertserini-bert-base-squad",
    "deepset/minilm-uncased-squad2",
    "dmis-lab/biobert-large-cased-v1.1-squad",
    "deepset/bert-base-cased-squad2",
    "bert-large-cased-whole-word-masking-finetuned-squad"
    ]


def QnA_on_custom_dataset(dataset, output_file):
    headers = ['question', 'model', 'gr_correct_answer', 'gr_model_answer', 'en_correct_answer', 'en_model_answer', 'model_response_time', 'confidence_score']
    write_headers(output_file, headers)

    for set in dataset:
        context = set['context']
        questions = set['questions']
        answers = set['answers']
        models = get_models()
        en_context = translate(context, translator, 'el', 'en')
        print('Context:', en_context)
        for i in range(len(questions)):
            en_question = translate(questions[i], translator, 'el', 'en')
            print('Question: ', en_question)
            result_rows = []
            for j in range(len(models)):
                result, elapsed_time = answer_question(en_context, en_question, models[j])
                gr_model_answer = translate(result['answer'], translator, src='en', dest='el')
                translated_correct_answer = translate(answers[i], translator, src='el', dest='en')
                result_rows.append([questions[i], models[j], answers[i], gr_model_answer, translated_correct_answer, result['answer'], elapsed_time, result['score']])
            with open(output_file, 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                for k in range(len(result_rows)):
                    writer.writerow(result_rows[k])


def QnA_on_xquad(dataset, output_file):
    pass

if __name__ == '__main__':
    input_dir = '../../../resources/json_files/'
    input_filename = select_input_file(input_dir)
    translator = select_translator()

    dataset = get_dataset(input_filename)

    if input_filename == 'custom_QnA_dataset.json':
        output_filename = 'QnA_on_custom_dataset_with_' + translator + '.csv'
        QnA_on_custom_dataset(dataset, output_filename)
    elif input_filename == 'squad_QnA_dataset.json':
        output_filename = 'QnA_on_xquad_with_' + translator + '.csv'
        QnA_on_xquad(dataset, output_filename)
    else:
        print("No man's land.")