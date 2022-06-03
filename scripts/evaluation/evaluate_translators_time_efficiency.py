import json
import os,sys,inspect
import time


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from utils import translator

input_json_filepath = '../../resources/json_files/greek_text_QnA_collection.json'

trans = 'helsinki'

f = open(input_json_filepath, encoding='utf16')
json_data = json.load(f)['collection']

# Large text evaluation


el_to_en = []
en_to_el = []

for context_with_qna in json_data[:2]:

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


print(el_to_en)
print(en_to_el)

