import json
import os,sys,inspect
import time


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from utils import translator

input_json_filepath = '../../resources/json_files/custom_QnA_dataset.json'

trans = 'bing'

f = open(input_json_filepath, encoding='utf16')
json_data = json.load(f)['collection']

# Large text evaluation


el_to_en = []
en_to_el = []

for context_with_qna in json_data[:2]:
    start = time.time()
    translated_text = translator.translate(context_with_qna['context'] , trans, 'el', 'en')
    end = time.time()
    el_to_en.append({"characters": len(context_with_qna['context']) , "time":(end-start) })

    for question in context_with_qna['questions']:
        # For el to en
        start = time.time()
        translated_text = translator.translate(question , trans, 'el', 'en')
        end = time.time()
        el_to_en.append({"characters": len(question) , "time":(end-start) })

        start = time.time()
        translated_text = translator.translate(translated_text, trans, 'en', 'el')
        end = time.time()
        en_to_el.append({"characters": len(question) , "time":(end-start) })

sum = 0
for dict in el_to_en:
    sum += dict['time']

for dict in en_to_el:
    sum += dict['time']

average_time = sum / (len(el_to_en) + len(en_to_el))
print('Average translation time of ' + trans + ' is ' + str(average_time) + ' seconds.')
