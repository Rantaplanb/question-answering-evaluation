from utils.translator import translate
from pathlib import Path

def apply_all_translators(text, input_lang, output_lang):
    translators = ["google", "helsinki", "textblob", "bing", "goslate", "google2"]
    print('Original text: \n', text, '\n')

    for translator in translators:
        print(translator, ":")
        print(translate(text, translator, input_lang, output_lang), '\n')
    print('------------------------------------------------------------')

def get_contexts():
    f = open('../resources/txt_files/delimited_contexts.txt')
    unedited_input = f.read()
    contexts = unedited_input.split("[delimiter]")
    contexts.pop(len(contexts) - 1)
    f.close()
    return contexts

if __name__ == "__main__":
    texts = Path('../resources/txt_files/texts_for_translation.txt').read_text()
    texts = texts.split('//delimiter')
    for text in texts:
        apply_all_translators(text, 'el', 'en')

    contexts = get_contexts()
    for context in contexts:
        apply_all_translators(context, 'el', 'en')