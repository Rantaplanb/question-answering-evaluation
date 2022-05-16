import pandas as pd

df_bing = pd.read_csv('../resources/csv_files/questions_with_answers_from_all_models_on_our_collection_bing.csv', encoding='utf16')
df_helsinki = pd.read_csv('../resources/csv_files/questions_with_answers_from_all_models_on_our_collection.csv', encoding='utf16')

bing_model_evaluation = df_bing["is_correct"]
helsinki_model_evaluation = df_helsinki["is_correct"]

bing_questions = df_bing["question"]
helsinki_questions = df_helsinki["question"]

bing_prediction_score = df_bing['score']
helsinki_prediction_score = df_helsinki['score']

question_number = 10
model_number = 10

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

def get_translator(table):
    if table.equals(bing_model_evaluation) or table.equals(bing_questions):
        return 'Bing'
    else: 
        return 'Helsinki'

def get_specific_model_evaluation_histogram_table(model_answers, model):
    model_evaluation_count_table = {'model': model, 'translator': get_translator(model_answers), 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }
    model_index = models.index(model)

    for i in range(int(len(model_answers) / (question_number * model_number) )):
        # print('For the ', i , ' context: ')
        for j in range(question_number):
            current_index =  (i * model_number * question_number) + (j * question_number) + model_index
            # print(current_index)
            model_evaluation_count_table[model_answers[current_index]] += 1
    # print(model_evaluation_count_table)
    return model_evaluation_count_table

def get_specific_question_evaluation_histogram_table(model_answers, context_index, question_index):
    questions = bing_questions if model_answers.equals(bing_model_evaluation) else helsinki_questions
    starting_index = (context_index * model_number * question_number) + (question_index * question_number)
    question_evaluation_count_table = {'question': questions[starting_index], 'translator': get_translator(questions), 'yes': 0, 'no': 0, 'partially': 0, 'invalid':0 }

    for i in range(question_number):
        question_evaluation_count_table[model_answers[starting_index + i]] += 1

    return question_evaluation_count_table

def convert_model_is_correct_column(model_answers):
    for i in range(len(model_answers)):
        converted_num = 0
        if model_answers[i] == 'yes':
            converted_num = 1
        elif model_answers[i] == 'partially':
            converted_num = 0.5
        model_answers[i] = converted_num
    
    return model_answers

if __name__ == "__main__":
    for i in range(model_number):
        print(get_specific_model_evaluation_histogram_table(bing_model_evaluation, models[i]))
    
    print("")
    print(get_specific_question_evaluation_histogram_table(helsinki_model_evaluation, 19, 2))
    print(convert_model_is_correct_column(bing_model_evaluation).corr(bing_prediction_score))

    


    