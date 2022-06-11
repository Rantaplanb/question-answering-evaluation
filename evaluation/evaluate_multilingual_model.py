import spacy, csv, re
import pandas as pd
import Levenshtein
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util

input_file = '../../resources/csv_files/questions_with_answers_from_multilingual_model.csv'
output_file = '../../resources/csv_files/multilingual_model_qna_on_our_collection.csv'

def count_common_words(s0, s1):
    s0 = s0.lower()
    s1 = s1.lower()
    s0List = s0.split(" ")
    s1List = s1.split(" ")
    return len(list(set(s0List)&set(s1List)))

def evaluate_automatic_labeling(labeled_by_human, labeled_by_machine):
    correct_and_equal = 0
    correct_not_equal = 0
    partially_and_equal = 0
    partially_not_equal = 0
    wrong_and_equal = 0
    wrong_not_equal = 0
    for index in range(len(labeled_by_machine)):
        manual = labeled_by_human[index]
        automatic = labeled_by_machine[index]
        if manual == 'invalid':
            continue
        elif manual == 'yes':
            if manual == automatic:
                correct_and_equal += 1
            else:
                correct_not_equal += 1
        elif manual == 'partially':
            if manual == automatic:
                partially_and_equal += 1
            else:
                partially_not_equal += 1
        elif manual == 'no':
            if manual == automatic:
                wrong_and_equal += 1
            else:
                wrong_not_equal += 1
    print('The corrected labeled answers were: ', correct_and_equal + wrong_and_equal + partially_and_equal)
    print('The wrong labeled answers were: ', correct_not_equal + wrong_not_equal + partially_not_equal)
    print('Wrongly labeled correct questions were: ', correct_not_equal)
    print('Wrongly labeled partially correct questions were: ', partially_not_equal)
    print('Wrongly labeled wrong questions were: ', wrong_not_equal)

def score_to_label(answer_score):
        if float(answer_score) > 0.5:
            return 'yes'
        elif float(answer_score) > 0.4:
            return 'partially'
        else:
           return 'no'

data = pd.read_csv(input_file, encoding='UTF-16')
model_answers = data['model_answer']
correct_answers = data['correct_answer']
questions = data['question']
model_prediction_scores = data['confidence_score']
model_response_times = data['model_response_time']

model_response_times = list(model_response_times)
model_response_times.sort()
resp_time_total = 0
for i in range(len(model_response_times)):
    resp_time_total += model_response_times[i]
average_response_time = resp_time_total / len(model_response_times)
median_response_time = model_response_times[int(len(model_response_times) / 2)]
print('Average response time: ', average_response_time)
print('Median response time: ', median_response_time)

nlp = spacy.load("en_core_web_lg")
sentence_transformer = SentenceTransformer('distilbert-base-nli-mean-tokens')
sentence_transformer_multilingual = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased')

headers = ['question', 'model_answer', 'correct_answer', 'model_prediction_score', 'multilingual_sentence_transformers_score', 'is_correct (labeled by machine)', 'is_correct (labeled by human)']
with open(output_file, 'a', encoding='UTF16') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for i in range(int(len(model_answers))):
        model_answer = model_answers[i]
        correct_answer = correct_answers[i]

        # levenshtein_distance = Levenshtein.distance(model_answer, correct_answer)
        # levenshtein_score = float("{:.3f}".format(1 - ( float(levenshtein_distance) / (max(len(model_answer), len(correct_answer))))))

        # nlp_score = float("{:.3f}".format(nlp(model_answer).similarity(nlp(correct_answer))))

        # substring_score = float("{:.3f}".format(SequenceMatcher(None, model_answer, correct_answer).ratio()))

        # sentence_embeddings = sentence_transformer.encode([model_answer, correct_answer])
        # sentence_transformers_score = float("{:.3f}".format(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])[0][0].item()))
        
        # common_words = count_common_words(model_answer, correct_answer)
        # precision = common_words / len(model_answer.split(" "))
        # recall = common_words / len(correct_answer.split(" "))
        # f1_score = 0 if precision == 0 and recall == 0 else (2 * precision * recall) / (precision + recall)

        # weighted_score = nlp_score * 0.2 + levenshtein_score * 0.1 + substring_score * 0.1 + sentence_transformers_score * 0.4 + f1_score * 0.2

        sentence_embeddings = sentence_transformer_multilingual.encode([model_answer, correct_answer])
        multilingual_sentence_transformers_score = float("{:.3f}".format(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])[0][0].item()))

        writer.writerow([questions[i], model_answer.replace(";", ""), correct_answer.replace(";",""), model_prediction_scores[i], multilingual_sentence_transformers_score, score_to_label(multilingual_sentence_transformers_score), '-'])