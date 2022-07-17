import sparknlp

from pyspark.ml import PipelineModel
from sparknlp.annotator import *
from sparknlp.base import *

spark = sparknlp.start(spark32 = True)
documenter = DocumentAssembler().setInputCol("text").setOutputCol("document")
sentencerDL = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "xx").setInputCols(["document"]).setOutputCol("sentences")
sd_model = LightPipeline(PipelineModel(stages=[documenter, sentencerDL]))

def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

def split_to_sentences(text):
    sentences=[]
    for anno in sd_model.fullAnnotate(text)[0]["sentences"]:
        sentences.append(anno.result)
    res = []
    for sent in sentences:
        if len(sent) > 999:
            str_index = findnth(sent, ' ', int(sent.count(' ') / 2))
            res.append(sent[0:str_index])
            res.append(sent[str_index:])
        else:
            res.append(sent)
    return res


def split_text(text, length_limit):
    sentences = split_to_sentences(text)
    texts = []
    char_counter = 0
    cur_text = ''
    for sentence in sentences:
        if char_counter + len(sentence) > length_limit:
            texts.append(cur_text)
            cur_text = ''
            char_counter = 0
        cur_text += sentence
        char_counter += len(sentence)
    texts.append(cur_text)
    return texts