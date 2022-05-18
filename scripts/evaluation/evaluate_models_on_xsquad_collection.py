import spacy, csv, re
import pandas as pd
import Levenshtein
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util

input_file = '../../resources/csv_files/questions_with_answers_from_all_models_with_helsinki_cleaned.csv'
output_file = '../../resources/csv_files/questions_with_answers_from_all_models_on_xsquad_bing.csv'

def count_common_words(s0, s1):
    s0 = s0.lower()
    s1 = s1.lower()
    s0List = s0.split(" ")
    s1List = s1.split(" ")
    return len(list(set(s0List)&set(s1List)))

data = pd.read_csv(input_file, encoding='UTF-16')
model_answers = data['original_model_answer']
correct_answers = data['translated_correct_answer']
questions = data['question']
models = data['model'][:10]
model_prediction_scores = data['score']

nlp = spacy.load("en_core_web_lg")
sentence_transformer = SentenceTransformer('distilbert-base-nli-mean-tokens')

headers = ['question', 'model', 'model_answer', 'correct_answer', 'model_prediction_score', 'nlp_score', 'levenshtein_score', 'substring_score', 'sentence_transformers_score', 'F1_score', 'weighted_total_score']

greek_to_english = {}

with open(output_file, 'a', encoding='UTF16') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    print('Model answers count: ', len(model_answers))
    for i in range(int(len(model_answers) / 10)):
        write_format_flag = True
        weighted_scores = []
        for j in range(10):
            model_answer = model_answers[i*10 + j]
            correct_answer = correct_answers[i*10 + j]

            #Calculate scores:
            levenshtein_distance = Levenshtein.distance(model_answer, correct_answer)
            levenshtein_score = float("{:.3f}".format(1 - ( float(levenshtein_distance) / (max(len(model_answer), len(correct_answer))))))

            nlp_score = float("{:.3f}".format(nlp(model_answer).similarity(nlp(correct_answer))))

            substring_score = float("{:.3f}".format(SequenceMatcher(None, model_answer, correct_answer).ratio()))

            sentence_embeddings = sentence_transformer.encode([model_answer, correct_answer])
            sentence_transformers_score = float("{:.3f}".format(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])[0][0].item()))
            
            print("model_answer: ", model_answer)
            print("correct_answer: ", correct_answer)
            common_words_count = count_common_words(model_answer, correct_answer)
            precision = common_words_count / len(model_answer.split(" "))
            recall = common_words_count / len(correct_answer.split(" "))
            f1_score = 0 if precision == 0 and recall == 0 else (2 * precision * recall) / (precision + recall)

            weighted_score = nlp_score * 0.3 + levenshtein_score * 0.2 + substring_score * 0.2 + sentence_transformers_score * 0.2 + f1_score * 0.1
            weighted_scores.append(weighted_score)

            if write_format_flag is True:
                writer.writerow([questions[i*10], models[j], model_answer, correct_answer, model_prediction_scores[i*10 + j], nlp_score, levenshtein_score, substring_score, sentence_transformers_score, f1_score, weighted_score])
                write_format_flag = False           
            else:
                writer.writerow(['', models[j], model_answer, correct_answer, model_prediction_scores[i*10 + j], nlp_score, levenshtein_score, substring_score, sentence_transformers_score, f1_score, weighted_score])