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
    elif filename == 'demo_QnA_dataset.json':
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

def select_translator():
    if '-trans' in sys.argv:
        return sys.argv[sys.argv.index('-trans') + 1]
    print('The available translators are:\n1) Bing\n2) Helsinki ')
    choice = input('Select translator number: ')
    if choice.isdigit() and int(choice) > 0 and int(choice) <= 2:
        return 'bing' if choice == 1 else 'helsinki'
    else:
        print('Invalid input, expected number in range of (0 - 2)')
        print('Terminating ...')
        exit(0)

def select_models():
    if '--models' in sys.argv:
        model_count = 1
        models = []
        while True:
            if '-m' + str(model_count) not in sys.argv:
                break
            models.append(sys.argv.index('-m' + str(model_count)) + 1)
        return models
    else:
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
            "bert-large-cased-whole-word-masking-finetuned-squad", 
            "deepset/tinyroberta-squad2"
        ]


def QnA_on_custom_dataset(dataset, output_file, models):
    headers = ['question', 'model', 'gr_correct_answer', 'gr_model_answer', 'en_correct_answer', 'en_model_answer', 'model_response_time', 'confidence_score']
    write_headers(output_file, headers)

    for set in dataset:
        context = set['context']
        questions = set['questions']
        answers = set['answers']
        en_context = translate(context, translator, 'el', 'en')
        print('Context:', en_context)
        for i in range(len(questions)):
            en_question = translate(questions[i], translator, 'el', 'en')
            print('Question: ', en_question)
            result_rows = []
            question = en_question
            for j in range(len(models)):
                result, elapsed_time = answer_question(en_context, en_question, models[j])
                gr_model_answer = translate(result['answer'], translator, src='en', dest='el')
                en_correct_answer = translate(answers[i], translator, src='el', dest='en')
                result_rows.append([question, models[j], answers[i], gr_model_answer, en_correct_answer, result['answer'], elapsed_time, result['score']])
                question = ''
            with open('../output_data/' + output_file, 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                for k in range(len(result_rows)):
                    writer.writerow(result_rows[k])
                    

def QnA_on_xquad(dataset, output_file, models):
    headers = ['question', 'model', 'gr_correct_answer', 'gr_model_answer', 'en_correct_answer', 'en_model_answer', 'model_response_time', 'confidence_score']
    write_headers(output_file, headers)

    for subject in dataset:
        paragraphs = subject["paragraphs"]
        for QnA in paragraphs:      
            en_context = translate(QnA['context'], translator, 'el', 'en')
            print('Context:', en_context)
            for qna in QnA["qas"]:
                en_question = translate(qna["question"], translator, 'el', 'en')
                print('Question: ', en_question)
                result_rows = []
                question = en_question
                for i in range(len(models)):
                    result, elapsed_time = answer_question(en_context, en_question, models[i])
                    gr_model_answer = translate(result['answer'], translator, src='en', dest='el')
                    en_correct_answer = translate(qna['answers'][0]['text'], translator, src='el', dest='en')
                    result_rows.append([question, models[i], qna['answers'][0]['text'], gr_model_answer, en_correct_answer, result['answer'], elapsed_time, result['score']])
                    question = ""
                with open('../output_data/' + output_file, 'a', encoding='UTF16') as file:
                    writer = csv.writer(file)
                    for j in range(len(result_rows)):
                        writer.writerow(result_rows[j])


def QnA_on_demo_dataset(dataset, output_file):
    QnA_on_custom_dataset(dataset, output_file)

"""
---Script Configuration---
- To execute question answering with a different BERT model set, 
  just modify the model list that is returned by get_models() function.
- To add your own input QnA dataset:
    1) Add your own json file to the ${PROJECT_ROOT}/resources/json_files/ directory.
    2) Modify get_dataset() to load your json file.
    3) Implement your own QnA_on_${DATASET_NAME} function using answer_question(). 
    4) Add a case in main() for your json dataset and call your function implemented in (3).
"""
if __name__ == '__main__':
    input_dir = '../../../resources/json_files/'
    input_filename = select_input_file(input_dir)
    translator = select_translator()
    models = select_models()

    dataset = get_dataset(input_filename)

    if input_filename == 'custom_QnA_dataset.json':
        output_filename = 'QnA_on_custom_dataset_with_' + translator + '.csv'
        QnA_on_custom_dataset(dataset, output_filename, models)
    elif input_filename == 'squad_QnA_dataset.json':
        output_filename = 'QnA_on_xquad_with_' + translator + '.csv'
        QnA_on_xquad(dataset, output_filename, models)
    elif input_filename == 'demo_QnA_dataset.json':
        output_filename = 'QnA_on_demo_dataset_with_' + translator + '.csv'
        QnA_on_demo_dataset(dataset, output_filename, models)
    else:
        print("No man's land.")