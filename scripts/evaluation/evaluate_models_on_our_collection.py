import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

translator = 'bing'
total_contexts = 20
questions_per_context = 10
model_count = 10

def get_data(translator):
    return pd.read_csv('../../resources/csv_files/questions_with_answers_from_all_models_on_our_collection_' + translator + '.csv', encoding='utf16')

data = get_data(translator)
is_correct_col = data['is_correct']
questions_col = data['question']
scores_col = data['score']

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

def get_model_results(model):
    results = {'model': model, 'translator': translator, 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }
    model_index = models.index(model)

    for i in range(total_contexts * questions_per_context):
        current_index = (i * questions_per_context) + model_index
        results[is_correct_col[current_index]] += 1
    return results


def get_question_results(context_index, question_index):
    starting_index = (context_index * model_count * questions_per_context) + (question_index * questions_per_context)
    results = {'question': questions_col[starting_index], 'translator': translator, 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }
    for i in range(questions_per_context):
        results[is_correct_col[starting_index + i]] += 1
    return results


def get_model_scores(model):
    model_index = models.index(model)
    scores = []
    for i in range(total_contexts * questions_per_context):
        current_index = (i * questions_per_context) + model_index
        scores.append(scores_col[current_index])
    return scores

def print_basic_model_statistics(model_results):
    pass

def print_basic_question_statistics(question_results):
    pass

if __name__ == "__main__":
    model_results = []
    for i in range(model_count):
        model_results.append(get_model_results(models[i]))

    question_results = []
    for i in range(total_contexts):
        for j in range(questions_per_context):
            question_results.append(get_question_results(i, j))

    

    # converted_bing_model_evaluation = convert_model_is_correct_column_to_num(bing_model_evaluation)

    # r = np.corrcoef(np.array(converted_bing_model_evaluation), np.array(bing_prediction_scores))
    # print(r)
    # plt.plot(converted_bing_model_evaluation, bing_prediction_scores)

    