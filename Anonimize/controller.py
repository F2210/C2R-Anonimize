import asyncio
import random
import time
from REST.models import *
from .db import *
from .language import NER, nerPerformer, debug
from .models import nermodels
import requests
import json
import langid
from multiprocessing import Process
from abydos.distance import LIG3

# start connection to database
cnx = startconnection()

# load models into memory
models = NER().nermodels

class de_identify(Process):

    def __init__(self, sentence, session):
        
        # self.models = models
        self.textdata: TextData = TextData.objects.get(id=sentence.id)
        self.session: Session = Session.objects.get(id=session.id)
        self.language: str = self.session.language
        self.entities: set = {i for i in Entity.objects.filter(session=self.session)}
        self.model: str = ""
        self.modeltype: str = ""
        self.snomed_edition: str = ""
        self.snomed_version: str = ""
        super(de_identify, self).__init__()

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
        print(self.language)

        self.NERDetection()
        print(self.entities)

        self.EntityClassification()
        print(self.entities)

        self.NEApplier()
        print(self.textdata.replacement_text)

    def languageProcessor(self):

        # Check if the language was already known
        if self.session.language is not None:
            language_code = self.session.language
        else:
            langid.set_languages(nermodels.keys())
            language_code, score = langid.classify(self.textdata.original_text)

        # Set language in class
        self.language = language_code

        (self.model, self.modeltype, self.snomededition) = models[self.language]

        # Save language to database
        self.session.language = language_code
        self.textdata.status = 1
        self.session.save()

    def NERDetection(self):

        if not debug:
            # Perform NER detection on sentence
            result_entities = nerPerformer(models[self.language], self.textdata.original_text)

            # Store entities in database
            self.textdata.entities = result_entities
            self.textdata.save()

        else:
            result_entities = Entity.objects.filter(session=self.session)

        # Go over entities to store them seperately
        for entity in result_entities:
            if not debug:
                entity_instance = Entity.objects.get_or_create(in_entity=entity, session=self.session, type_entity=result_entities[entity])[0]
            else:
                entity_instance = entity
            # add created entity to class
            self.entities.add(entity_instance)

        # Set status for sentence
        self.textdata.status = 2
        self.textdata.save()

    def EntityClassification(self):

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

            SIMDISTANCE = 0.85

            medical = False

            for result in response.json()["result"]:
                if entity in result["name"]:
                    medical = True
                for term in result["name"].split(" "):
                    if LIG3().sim(src=term, tar=entity) > SIMDISTANCE:
                        medical = True
                else:
                    medical = False

            if medical:
                entity.type_entity = "medical_domain"
            else:
                pass

    def NEApplier(self):

        # if the enity is not an eponym of a disease

        for entity in self.entities:
            names = ["Mark", "Tom", "Erik", "Peter"]

            int = random.randint(0, 4)
            if entity.out_entity is None:
                entity.out_entity = names[int]
                entity.save()

        sentence = self.textdata.original_text

        for entity in self.entities:
            sentence = sentence.lower().replace(entity.in_entity.lower(), entity.out_entity.lower())

        self.textdata.replacement_text = sentence
        self.textdata.save()

class re_identify(Process):

    def __init__(self, sentence, session):
        # self.models = models
        self.textdata = TextData.objects.get(id=sentence.id)
        self.retextdata: str = ""
        self.session: Session = Session.objects.get(id=session.id)
        self.entities: set = {i for i in Entity.objects.filter(session=self.session)}
        super(re_identify, self).__init__()

    def run(self):

        textdata = self.textdata.original_text

        for entity in self.entities:
            if entity.out_entity in textdata:
                textdata = textdata.replace(entity.out_entity, entity.in_entity)

        self.textdata.replacement_text = textdata
        self.textdata.save()
