import csv, json, requests
from utils.translator import translate
from transformers import pipeline
import time

input_file = '../resources/json_files/squad_QnA_dataset.json'
output_file = '../resources/csv_files/questions_with_answers_from_all_models.csv'

translator = 'bing'

def answer_question(context, question, model):
    start = time.time()
    question_answerer = pipeline(task="question-answering", model = model)
    answer = question_answerer(question = question, context = context)
    end = time.time()
    return answer, end-start

def fetch_data():
    response = requests.get("http://users.ics.forth.gr/mountant/files/greek.json")
    json_qna_str = response.text
    return json.loads(json_qna_str)["data"]

def get_dataset():
    f = open(input_file)
    return json.load(f)["data"]

print("Getting data...")
data = get_dataset()

headers = ['question', 'model', 'model_response_time', 'score', 'start', 'end', 'original_model_answer', 'translated_model_answer', 'correct_answer']

models = [
    "deepset/roberta-base-squad2",
    "bert-large-uncased-whole-word-masking-finetuned-squad",
    "distilbert-base-cased-distilled-squad",
    "deepset/bert-large-uncased-whole-word-masking-squad2",
    "distilbert-base-uncased-distilled-squad",
    "rsvp-ai/bertserini-bert-base-squad",
    "deepset/minilm-uncased-squad2",
    "dmis-lab/biobert-large-cased-v1.1-squad",
    "deepset/bert-base-cased-squad2",
    "bert-large-cased-whole-word-masking-finetuned-squad"]

with open(output_file, 'a', encoding='UTF16') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

for subject in data:
    paragraphs = subject["paragraphs"]
    print('\n-------------------------\n')
    for QnA in paragraphs:      
        en_context = translate(QnA['context'], translator, 'el', 'en')
        print('Context:', en_context)
        for qna in QnA["qas"]:
            en_question = translate(qna["question"], translator, 'el', 'en')
            print('Question: ', en_question)
            results = []
            question = en_question
            for i in range(len(models)):
                result, elapsed_time = answer_question(en_context, en_question, models[i])
                results.append([question, models[i], elapsed_time, result['score'], result['start'], result['end'], result['answer'], translate(result['answer'], translator, src='en', dest='el'), qna['answers'][0]['text']])
                question = ""
            with open(output_file, 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                for i in range(len(results)):
                    writer.writerow(results[i])