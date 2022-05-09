import csv, json, requests
from utils.translator import translate
from transformers import pipeline

print("Script starts...")
output_file = '../resources/csv_files/questions_with_answers_from_all_models_with_bing_translator.csv'

def answer_question(context, question, model):
    question_answerer = pipeline(task="question-answering", model = model)
    return question_answerer(question = question, context = context)

def fetch_data():
    response = requests.get("http://users.ics.forth.gr/mountant/files/greek.json")
    json_qna_str = response.text
    return json.loads(json_qna_str)["data"]

def get_dataset():
    f = open('../resources/json_files/squad_QnA_dataset.json')
    return json.load(f)["data"]

print("Getting data...")
data = get_dataset()

headers = ['question', 'model', 'score', 'start', 'end', 'translated_model_answer', 'original_model_answer', 'correct_answer']

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
    for QnA in paragraphs: #For each context 
        en_context = translate(QnA['context'], 'bing', 'el', 'en') 
        print('Context:', en_context)
        for qna in QnA["qas"]: #For each question
            en_question = translate(qna["question"], 'bing', 'el', 'en')
            print('Question: ', en_question)
            results = []
            question = en_question
            for i in range(len(models)): #For each model
                result = answer_question(en_context, en_question, models[i])
                results.append([question, models[i], result['score'], result['start'], result['end'], result['answer'], translate(result['answer'], 'bing', src='en', dest='el'), qna['answers'][0]['text']])
                question = ""

            with open(output_file, 'a', encoding='UTF16') as file:
                writer = csv.writer(file)
                for i in range(len(results)): #For each model answer
                    writer.writerow(results[i])