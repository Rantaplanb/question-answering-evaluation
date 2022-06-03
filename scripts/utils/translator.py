from googletrans import Translator
import translators as ts
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,pipeline
import goslate
from textblob import TextBlob
from utils.sentenceDetector import splitToSentences, splitText
import time

# google_translator = Translator()

tokenizer_gr_to_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-grk-en")
model_gr_to_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-grk-en")

tokenizer_en_to_gr = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-el")
model_en_to_gr = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-el")

# goslate_translator = goslate.Goslate()

# Map greek and english words.
greek_to_english = {}

def google_translate(input, src='auto', dest='en'):
    result = ''
    if len(input) > 2500:
        texts = splitText(input, 2500)
        for text in texts:
            result += google_translator.translate(text, src=src, dest=dest).text
    else:
        result = google_translator.translate(input, src=src, dest=dest).text
    return result

def translate_sentence_with_helsinki(input, src='el', dest='en'):
    if ( (src == 'el') and (dest == 'en') ):
        translation=pipeline("translation",model=model_gr_to_en,tokenizer=tokenizer_gr_to_en)
    elif ( (src == 'en') and (dest == 'el') ):
        translation=pipeline("translation",model=model_en_to_gr,tokenizer=tokenizer_en_to_gr)
    else:
        raise Exception("Invalid language selection.")
    return translation(input)[0]['translation_text']

def helsinki_translate(text, input_lang, output_lang):
    sentences = splitToSentences(text)
    translated_text = ''
    for sentence in sentences:
        if(sentence == '..'):
            translated_text += '..'
        else:
            if sentence not in greek_to_english.keys():
                greek_to_english[sentence] = translate_sentence_with_helsinki(sentence, input_lang, output_lang)
                print('Appending to dictionary:', sentence, '->', translated_text)
            else:
                print('Using from dictionary: ', sentence, '->', greek_to_english[sentence])
            translated_text += greek_to_english[sentence]
    return translated_text

def goslate_translate(input, src='auto', dest='en'):
    return goslate_translator.translate(input, dest)

def textblob_translate(input, src='auto', dest='en'):
    return TextBlob(input).translate(to=dest)

def google2_translate(input, src='auto', dest='en'):
    return ts.google(input, from_language=src, to_language=dest)

def request_bing_translation(input, src, dest):
    nap_time = 3
    exception_counter = 0
    exception_total_counter = 0
    while(True):
        try:
            if exception_total_counter > 100:
                print("Reached 100 exceptions sleeping for 2 minutes...")
                time.sleep(120)
                exception_total_counter = 0
            response = ts.bing(input, from_language=src, to_language=dest)
            return response
        except Exception as e:
            if(exception_counter > 5):
                nap_time += nap_time
            exception_counter += 1
            exception_total_counter += 1
            print("An exception occured: ", e)
            print("Sleeping for ", nap_time, ", exceptions happend: ", exception_counter)
            time.sleep(nap_time)


def bing_translate(input, src='auto', dest='en'):
    result = ''
    print("Original Text word count: ", len(input))
    if len(input) > 999:
        texts = splitText(input, 999)
        for text in texts:
            # if text not in greek_to_english.keys():
            translated_text = request_bing_translation(text, src, dest)
            result += translated_text
            #     print('Appending to dictionary:', text, '->', translated_text)
            #     greek_to_english[text] = translated_text
            # else:
            #     result += greek_to_english[text]
    else:
        if input not in greek_to_english.keys():
            translated_text = request_bing_translation(input, src, dest)
            result = translated_text
            print('Appending to dictionary:', input, '->', translated_text)
            greek_to_english[input] = translated_text
        else:
            print('Using from dictionary: ', input, '->', greek_to_english[input])
            result += greek_to_english[input]
    return result

# Dictionary of functions
translate_dict = {
    "google": google_translate,
    "helsinki": helsinki_translate,
    "goslate": goslate_translate,
    "textblob": textblob_translate,
    "google2": google2_translate,
    "bing": bing_translate
}

def translate(input, translator, src='el', dest='en'):
    try:
        return translate_dict[translator](input, src, dest)
    except Exception as e:
        print("Exception while translating: ",input, ", with translator: ", translator, " : ",e)
        return e

