import csv, json, requests
from transformers import pipeline
import time

def answer_question(context, question, model):
    start = time.time()
    question_answerer = pipeline(task="question-answering", model = model)
    answer = question_answerer(question = question, context = context)
    end = time.time()
    return answer, end-start


def get_dataset(filename):
    f = open('../../resources/json_files/' + filename + '.json', encoding='utf-16')
    if filename == 'greek_text_QnA_collection':
        return json.load(f)["collection"]
    elif filename == 'squad_QnA_dataset':
        return json.load(f)["data"]


def write_headers(filename, headers):
    with open('../../resources/csv_files/' + output_filename + '.csv', 'w', encoding='UTF16') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def QnA_on_custom_dataset(dataset, output_file):
    headers = ['question', 'model_answer', 'correct_answer', 'model_response_time', 'confidence_score', 'start', 'end']
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
            result_row = [question.replace(';', "?"), result['answer'].replace(',', ""), answers[i], elapsed_time, result['score'], result['start'], result['end']]
            question = ""
            with open('../../resources/csv_files/' + output_filename + '.csv', 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                writer.writerow(result_row)

def QnA_on_xquad_dataset(dataset, output_file):
    headers = ['question', 'model', 'model_response_time', 'score', 'start', 'end', 'original_model_answer', 'translated_model_answer', 'correct_answer']
    write_headers(output_file, headers)
    # with open(output_file, 'a', encoding='UTF16') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(headers)

    # for subject in data:
    #     paragraphs = subject["paragraphs"]
    #     print('\n-------------------------\n')
    #     for QnA in paragraphs:      
    #         en_context = translate(QnA['context'], translator, 'el', 'en')
    #         print('Context:', en_context)
    #         for qna in QnA["qas"]:
    #             en_question = translate(qna["question"], translator, 'el', 'en')
    #             print('Question: ', en_question)
    #             results = []
    #             question = en_question
    #             for i in range(len(models)):
    #                 result, elapsed_time = answer_question(en_context, en_question, models[i])
    #                 results.append([question, models[i], elapsed_time, result['score'], result['start'], result['end'], result['answer'], translate(result['answer'], translator, src='en', dest='el'), qna['answers'][0]['text']])
    #                 question = ""
    #             with open(output_file, 'a', encoding='UTF16') as file:
    #                 writer = csv.writer(file)
    #                 for j in range(len(results)):
    #                     writer.writerow(results[j])

if __name__ == '__main__':
    model = "deepset/xlm-roberta-large-squad2"
    input_filename = 'greek_text_QnA_collection'
    output_filename = 'questions_with_answers_from_multilingual_model'

    dataset = get_dataset(input_filename)

    if input_filename == 'greek_text_QnA_collection':
        QnA_on_custom_dataset(dataset, output_filename)
    elif input_filename == 'squad_QnA_dataset':
        QnA_on_xquad_dataset(dataset, output_filename)
    else:
        print("No man's land.")
    



