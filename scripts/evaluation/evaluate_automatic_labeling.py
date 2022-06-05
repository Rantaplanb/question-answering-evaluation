import pandas as pd

input_file = '../../resources/csv_files/2.evaluated_model_answers_csv/qna_on_our_collection_bing_scores_v2.csv'

data = pd.read_csv(input_file, encoding='UTF-16')

automatically_labeled = data['is_correct (labeled by machine)']
manually_labeled = data['is_correct (labeled by human)']

correct_and_equal = 0
correct_not_equal = 0
partially_and_equal = 0
partially_not_equal = 0
wrong_and_equal = 0
wrong_not_equal = 0
for index in range(len(automatically_labeled)):
    manual = manually_labeled[index]
    automatic = automatically_labeled[index]

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