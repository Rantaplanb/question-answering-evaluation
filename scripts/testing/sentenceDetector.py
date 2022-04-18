import sparknlp

from pyspark.ml import PipelineModel
from sparknlp.annotator import *
from sparknlp.base import *

spark = sparknlp.start(spark32 = True)
documenter = DocumentAssembler().setInputCol("text").setOutputCol("document")
sentencerDL = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "xx").setInputCols(["document"]).setOutputCol("sentences")
sd_model = LightPipeline(PipelineModel(stages=[documenter, sentencerDL]))

def splitText(text):
    sentences=[]
    for anno in sd_model.fullAnnotate(text)[0]["sentences"]:
        sentences.append(anno.result)
    return sentences