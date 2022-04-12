import pandas as pd

data = pd.read_csv('../resources/csv_files/model_scores_with_F1score.csv', encoding='UTF-16')

questions = data['question']

question_list = []

for i in range(int(len(questions) / 10)):
    print(i, questions[i*10])
