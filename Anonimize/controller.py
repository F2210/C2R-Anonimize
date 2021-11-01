import asyncio
import time
from REST.models import *
from .db import *
from .language import NER, nerPerformer
from .models import nermodels
import langid
from multiprocessing import Process

# start connection to database
cnx = startconnection()

# load models into memory
models = NER().nermodels

class Anonimize(Process):

    def __init__(self, sentence, session, client, caregiver):
        
        # self.models = models
        self.sentence = Sentence.objects.get(id=sentence.id)
        self.session = Session.objects.get(id=session.id)
        self.client = Client.objects.get(id=client.id)
        self.caregiver = Caregiver.objects.get(id=caregiver.id)
        self.language: str = self.session.language

        super(Anonimize, self).__init__()

    def run(self):

        # do stuff

        """
        :returns None
        step 1: perform language recognition on the sentence and try to get the language from the database.
        step 2: perform NER and set entities in database.
        step 3: classify the entities and decide whether they should be anonimized in the output after C2R processing.
        step 4: anonimze the text with placeholders.
        """
        self.languageProcessor()

        self.NERDetection()
        print(self)

        self.NERProcessing()
        print(self)

        self.NERApplier()
        print(self)

    def languageProcessor(self):

        # Check if the language was already known
        if self.session.language is not None:
            language_code = self.session.language
        else:
            langid.set_languages(nermodels.keys())
            language_code, score = langid.classify(self.sentence.original_text)

        # Set language in class
        self.language = language_code

        # Save language to database
        self.session.language = language_code
        self.sentence.status = 1
        self.session.save()

    def NERDetection(self):

        # Perform NER detection on sentence
        result_entities = nerPerformer(models[self.language], self.sentence.original_text)

        # Store entities in database
        self.sentence.entities = result_entities
        self.sentence.save()

        # Go over entities to store them seperately
        for entity in result_entities:
            Entity.objects.get_or_create(in_entity=entity, session=self.session, type_entity=result_entities[entity])

        # Set status for sentence
        self.sentence.status = 2
        self.sentence.save()

    def NERProcessing(self):
        pass

    def NERApplier(self):

