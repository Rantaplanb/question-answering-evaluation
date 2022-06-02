import pandas as pd
import re

input_file = '../resources/csv_files/questions_with_answers_from_all_models_on_xsquad_helsinki_v2.csv'
output_file = '../resources/csv_files/questions_with_answers_from_all_models_on_xsquad_helsinkii_with_is_correct.csv'



data = pd.read_csv(input_file, encoding='UTF-16')

weighted_scores = data['weighted_total_score']
is_correct = []
for answer in weighted_scores:
    print(answer)
    if float(answer) > 0.68:
        is_correct.append('yes')
    elif float(answer) > 0.5:
        is_correct.append('partially')
    else:
        is_correct.append('no')

data['is_correct'] = is_correct
data.to_csv(output_file, sep=',', encoding='UTF-16', index=False)