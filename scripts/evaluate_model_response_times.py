import pandas as pd

input_file = '../resources/csv_files/questions_with_answers_from_all_models_with_helsinki_cleaned.csv'
output_file = '../resources/csv_files/tmp.csv'

data = pd.read_csv(input_file, encoding='UTF-16')

response_times = data['model_response_time']

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
model_average_resp_times = [0,0,0,0,0,0,0,0,0,0]
model_median_resp_times = [[],[],[],[],[],[],[],[],[],[]]
for i in range(len(response_times)):
    model_average_resp_times[i % 10] += response_times[i]
    model_median_resp_times[i % 10].append(response_times[i])

print("Average response times:")
for i in range(len(model_average_resp_times)):
    print(models[i], ' -> ', model_average_resp_times[i] / (len(response_times) / 10), ' seconds')


print("\nMedian times:")
for i in range(len(model_median_resp_times)):
    model_median_resp_times[i].sort()
    print(models[i], ' -> ', model_median_resp_times[i][int(len(model_median_resp_times[i]) / 2)], ' seconds')