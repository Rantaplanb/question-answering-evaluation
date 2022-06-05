import pandas as pd
import re

input_file = '../resources/csv_files/2.evaluated_model_answers_csv/qna_on_our_collection_bing_scores.csv'
output_file = '../resources/csv_files/2.evaluated_model_answers_csv/temp.csv'



data = pd.read_csv(input_file, encoding='UTF-16')

weighted_scores = data['weighted_total_score']
is_correct = []
for answer in weighted_scores:
    print(answer)
    if float(answer) > 0.65:
        is_correct.append('yes')
    elif float(answer) > 0.5:
        is_correct.append('partially')
    else:
        is_correct.append('no')

data['is_correct (labeled by machine)'] = is_correct
data.to_csv(output_file, sep=',', encoding='UTF-16', index=False)