import csv, json, requests
from transformers import pipeline
import time

input_file = '../../resources/json_files/greek_text_QnA_collection.json'
output_file = '../../resources/csv_files/questions_with_answers_from_multilingual_model.csv'

def answer_question(context, question, model):
    start = time.time()
    question_answerer = pipeline(task="question-answering", model = model)
    answer = question_answerer(question = question, context = context)
    end = time.time()
    return answer, end-start


def get_dataset():
    f = open(input_file, encoding='utf-16')
    return json.load(f)["collection"]


print("Getting data...")
sets = get_dataset()

headers = ['question', 'model_answer', 'correct_answer', 'model_response_time', 'confidence_score', 'start', 'end']

model = "deepset/xlm-roberta-large-squad2"

with open(output_file, 'w', encoding='UTF16') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

for set in sets:
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
        with open(output_file, 'a', encoding='UTF16') as file:
            writer = csv.writer(file)
            writer.writerow(result_row)