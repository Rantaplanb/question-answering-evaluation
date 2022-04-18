from googletrans import Translator
import translators as ts
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,pipeline
import goslate
from textblob import TextBlob
from utils.sentenceDetector import splitToSentences, splitText

google_translator = Translator()

tokenizer_gr_to_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-grk-en")
model_gr_to_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-grk-en")

tokenizer_en_to_gr = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-el")
model_en_to_gr = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-el")

goslate_translator = goslate.Goslate()

def google_translate(input, src='auto', dest='en'):
    result = ''
    if len(input) > 2500:
        texts = splitText(input)
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
            translated_text += translate_sentence_with_helsinki(sentence, input_lang, output_lang)
    return translated_text

def goslate_translate(input, src='auto', dest='en'):
    return goslate_translator.translate(input, dest)

def textblob_translate(input, src='auto', dest='en'):
    return TextBlob(input).translate(to=dest)

def google2_translate(input, src='auto', dest='en'):
    return ts.google(input, from_language=src, to_language=dest)


def bing_translate(input, src='auto', dest='en'):
    return ts.bing(input, from_language=src, to_language=dest)

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
        return e

