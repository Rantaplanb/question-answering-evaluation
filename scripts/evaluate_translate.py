import requests, json

from utils.translator import translate
from pathlib import Path

def apply_all_translators(text, input_lang, output_lang):
    translators = ["google", "helsinki", "goslate", "textblob", "google2", "bing"]
    print('Original text: \n', text, '\n')

    for translator in translators:
        print(translator, ":")
        print(translate(text, translator, input_lang, output_lang), '\n')
    print('------------------------------------------------------------')


if __name__ == "__main__":
    texts = Path('../resources/txt_files/texts_for_translation.txt').read_text()
    texts = texts.split('//delimiter')
    for text in texts:
        apply_all_translators(text, 'el', 'en')

    # collection = requests.get("http://users.ics.forth.gr/mountant/files/greek.json").text
    # data = json.loads(collection)
    # for x in data["data"]:
    #     paragraphs=x["paragraphs"]
        
    #     for y in paragraphs:
    #         greek_context = y['context']
    #         apply_all_translators(greek_context, 'el', 'en')