import csv, json, requests
from utils.translator import translate
from transformers import pipeline
import time

input_file = '../resources/json_files/greek_text_QnA_collection.json'
output_file = '../resources/csv_files/questions_with_answers_from_all_models_on_our_collection_bing.csv'

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
    f = open(input_file, encoding='utf-16')
    return json.load(f)["collection"]

print("Getting data...")
sets = get_dataset()

headers = ['question', 'model', 'model_response_time', 'score', 'start', 'end', 'original_model_answer', 'translated_model_answer', 'correct_answer', 'translated_correct_answer']

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

for set in sets:
    context = set['context']
    questions = set['questions']
    answers = set['answers']

    en_context = translate(context, translator, 'el', 'en')
    print('Context:', en_context)
    for i in range(len(questions)):
        en_question = translate(questions[i], translator, 'el', 'en')
        print('Question: ', en_question)
        results = []
        tmp_question = en_question
        for j in range(len(models)):
            result, elapsed_time = answer_question(en_context, en_question, models[j])
            gr_model_answer = translate(result['answer'], translator, src='en', dest='el')
            translated_correct_answer = translate(answers[i], translator, src='el', dest='en')
            results.append([tmp_question, models[j], elapsed_time, result['score'], result['start'], result['end'], result['answer'], gr_model_answer, answers[i], translated_correct_answer])
            tmp_question = ""
        with open(output_file, 'a', encoding='UTF16') as file:
            writer = csv.writer(file)
            for k in range(len(results)):
                writer.writerow(results[k])