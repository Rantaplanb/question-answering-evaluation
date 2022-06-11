import statistics
import pandas as pd
import Levenshtein
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,pipeline

data = pd.read_csv('../resources/csv_files/questions_with_answers_from_all_models_on_xsquad_helsinki_with_is_correct_v2.csv', encoding='UTF-16')
questions = data['question']
models = data['model'][:10]
model_answers = data['model_answer']
correct_answers = data['correct_answer']
model_prediction_scores = data['score']
nlp_scores = data['nlp_score']
levenshtein_scores = data['levenshtein_score']
substring_scores = data['substring_score']
sentence_transformers_scores = data['sentence_transformers_score']
weighted_scores = data['weighted_total_score']
is_correct_col = data['is_correct']

total_weighted_score = []
average_model_prediction_score = []
model_prediction_accuracy = [] 
correct_answers_approximation = []
wrong_answers_approximation = []
partially_correct_answers_approximation = []
model_scores = []
model_predictions = []

for i in range(10):
    total_weighted_score.append(0)
    average_model_prediction_score.append(0)
    model_prediction_accuracy.append(0)
    correct_answers_approximation.append(0)
    wrong_answers_approximation.append(0)
    partially_correct_answers_approximation.append(0)
    model_scores.append([])
    model_predictions.append([])

for i in range(len(weighted_scores)):
    model_index = i % 10
    model_scores[model_index].append(weighted_scores[i])
    model_predictions[model_index].append(float(model_prediction_scores[i]))
    total_weighted_score[model_index] += weighted_scores[i]
    average_model_prediction_score[model_index] += float(model_prediction_scores[i])
    model_prediction_accuracy[model_index] += abs(weighted_scores[i] - float(model_prediction_scores[i]))
    if is_correct_col[i] == 'yes':
        correct_answers_approximation[model_index] += 1
    elif is_correct_col[i] == 'no':
        wrong_answers_approximation[model_index] += 1
    else:
        partially_correct_answers_approximation[model_index] += 1
    
total_weighted_score_avg = []
average_model_prediction_score_avg = []
model_prediction_accuracy_avg = []

total_questions = (i + 1) / 10
for i in range(10):
    total_weighted_score_avg.append(total_weighted_score[i] / total_questions)
    average_model_prediction_score_avg.append(average_model_prediction_score[i] / total_questions)
    model_prediction_accuracy_avg.append(model_prediction_accuracy[i] / total_questions)

for i in range(10):
    print('Statistics for the model: ', models[i])
    print('    Average total weighted score: ', total_weighted_score_avg[i])
    print('    Median total weighted score: ', statistics.median(model_scores[i]))
    print('    Average model prediction score: ', average_model_prediction_score_avg[i])
    print('    Median model prediction score: ', statistics.median(model_predictions[i]))
    print('    Average prediction fault: ', model_prediction_accuracy_avg[i])
    print('    Approximation of correct answers: ', correct_answers_approximation[i], '/', int(total_questions))
    print('    Approximation of correct answers: ', wrong_answers_approximation[i], '/', int(total_questions))
    print('    Approximation of correct answers: ', partially_correct_answers_approximation[i], '/', int(total_questions))
    print('---------------------------------------------------------------------------------')