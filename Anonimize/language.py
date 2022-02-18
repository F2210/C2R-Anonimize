from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from flair.data import Sentence
from flair.models import SequenceTagger
from .models import nermodels
from .resultProcessors import flair as flairType
from .resultProcessors import pipeline as pipelineType

debug = False

def nerPerformer(processdata, text):
    """

    :param processdata: tuple containing (pipeline or flair, sentenceprocessor, modeltype)
    :param text: string containing the to-be processed data
    :return: processed resultdata with each word and their type
    """
    (x, y, z) = processdata

    if z == "flair":
        tagger = x
        Sentence = y

        sentence = Sentence(text)

        tagger.predict(sentence)

        rawresult = sentence.get_spans("ner")

        result = flairType.resultProcessor(text, rawresult)

    if z == "transformer":
        ner = x

        result = pipelineType.resultProcessor(text, ner(text))

    return result

class NER:

    def __init__(self):

        self.nermodels = {}

        # retrieve models
        for key, model in nermodels.items():
            (self.model, self.modeltype, self.snomededition, self.snomedreleasedate) = model
            if not debug:
                self.nermodels[key] = (self.getModel())
            else:
                self.nermodels[key] = ("", "", "")

    def getModel(self):

        if self.modeltype == "flair":
            tagger = SequenceTagger.load(self.model)

            returnvalue = (tagger, Sentence, self.modeltype)

        elif self.modeltype == "transformer":
            tokenizer = AutoTokenizer.from_pretrained(self.model)
            model = AutoModelForTokenClassification.from_pretrained(self.model)

            ner = pipeline("ner", model=model, tokenizer=tokenizer)

            returnvalue = (ner, "", self.modeltype)

        return returnvalue