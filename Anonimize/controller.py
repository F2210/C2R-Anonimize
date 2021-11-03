import asyncio
import time
from REST.models import *
from .db import *
from .language import NER, nerPerformer
from .models import nermodels
import requests
import json
import langid
from multiprocessing import Process

# start connection to database
cnx = startconnection()

# load models into memory
models = NER().nermodels

class Anonimize(Process):

    def __init__(self, sentence, session, client, caregiver):
        
        # self.models = models
        self.sentence: Sentence = Sentence.objects.get(id=sentence.id)
        self.session: Session = Session.objects.get(id=session.id)
        self.client: Client = Client.objects.get(id=client.id)
        self.caregiver: Caregiver = Caregiver.objects.get(id=caregiver.id)
        self.language: str = self.session.language
        self.entities: list = []
        self.model: str = ""
        self.modeltype: str = ""
        self.snomed_edition: str = ""
        self.snomed_version: str = ""
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

        self.EponymSearch()
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

        (self.model, self.modeltype, self.snomededition) = models[self.language]

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
            entity_instance = Entity.objects.get_or_create(in_entity=entity, session=self.session, type_entity=result_entities[entity])
            # add created entity to class
            self.entities.append(entity_instance)

        # Set status for sentence
        self.sentence.status = 2
        self.sentence.save()

    def NERProcessing(self):

        # check if data from client or caregiver are in the sentence and/or entities dict and store that inforation
        # as entity type 'personal data'
        personal_attrs = ["firstname", "lastname", "address", "country"]
        for person in [json.loads(self.client.data), json.loads(self.caregiver.data)]:
            for attr in personal_attrs:
                if person[attr] in self.entities:
                    pass

        # if item was found that was not captured by datamodel: add it to the entities lib.

    def EponymSearch(self):

        # set base data for snomed connection
        baseUrl = 'https://browser.ihtsdotools.org/snowstorm/snomed-ct'
        # set edition to use using edition depending on language
        edition = self.snomed_edition
        # set version to use version set per language
        version = self.snomed_version

        # loop over entities found in the sentence
        for entity in self.entities:
            url = baseUrl + '/browser/' + edition + '/' + version + '/concepts?term=' + entity.in_entity + '&activeFilter=true&offset=0&limit=50'
            response = requests.get(url)
            data = response.json()

        #

    def NERApplier(self):
        pass
