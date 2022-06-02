import pandas as pd
from utils import translator
import re

input_file = '../resources/csv_files/questions_with_answers_from_all_models_with_bing_translator.csv'
output_file = '../resources/csv_files/questions_with_answers_from_all_models_with_bing_cleaned.csv'

translator_name = 'bing'

#Checks if there are greek letters in the string:
def is_translatable(string):
    for char in string:
        if char.isalpha() and re.search('[α-ωΑ-Ω]', char):
            return True
    return False


data = pd.read_csv(input_file, encoding='UTF-16')

correct_answers = data['correct_answer']
translated_correct_answers = []
for answer in correct_answers:
    print(answer)
    if is_translatable(answer):
        translated_correct_answers.append(translator.translate(answer, translator_name, 'el', 'en'))
    else:
        translated_correct_answers.append(answer)

data['translated_correct_answer'] = translated_correct_answers
data.to_csv(output_file, sep=',', encoding='UTF-16', index=False)