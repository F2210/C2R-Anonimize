from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification, PreTrainedTokenizerFast
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

    del processdata

    result = None

    if z == "flair":
        tagger = x
        Sentence = y

        sentence = Sentence(text)

        tagger.predict(sentence)

        rawresult = sentence

        result = flairType.resultProcessor(text, rawresult)

    if z == "transformer":

        result = pipelineType.resultProcessor(text, x(text))

    if result is None:
        Exception("The model was not set correctly. The type has to be either Flair or Transformer.")

    print("returning")

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

        returnvalue = None

        if self.modeltype == "flair":
            tagger = SequenceTagger.load(self.model)

            returnvalue = (tagger, Sentence, self.modeltype)

        elif self.modeltype == "transformer":
            tokenizer = AutoTokenizer.from_pretrained(self.model)

            model = AutoModelForTokenClassification.from_pretrained(self.model)

            ner = pipeline("ner", model=model, tokenizer=tokenizer)

            returnvalue = (ner, "", self.modeltype)

        if returnvalue is None:
            Exception("The model was not set correctly. The type has to be either Flair or Transformer.")

        return returnvalue