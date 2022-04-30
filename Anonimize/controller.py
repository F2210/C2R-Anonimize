import datetime
import random
import uuid

from Anonimize.db import new_db_connection

from .language import NER, nerPerformer
from .models import nermodels
import json
import langid
from multiprocessing import Process

models = NER().nermodels

def updatevalue(table, column, id, value):

    # print(table, column, id, value)

    connection = new_db_connection()
    with connection.cursor() as c:
        c.execute(
            'UPDATE REST_{0} SET {1}=%s WHERE id=%s '.format(table, column),
            [value, str(id).replace("-", "")]
        )
        connection.commit()
        connection.close()

def addentity(entity, sessionid, entitytype):

    # print("adding entity")
    connection = new_db_connection()
    with connection.cursor() as c:
        c.execute(
            'SELECT COUNT(id) FROM REST_entity '
            'WHERE in_entity=%s AND session_id=%s',
            [entity, str(sessionid).replace("-", "")]
        )
        result = c.fetchone()
        connection.commit()
        connection.close()

    (count, ) = result

    connection = new_db_connection()
    if count == 1:
        with connection.cursor() as c:
            c.execute(
                'SELECT * FROM REST_entity '
                'WHERE in_entity=%s ',
                [entity]
            )
            result = dict(zip([column[0] for column in c.description], c.fetchone()))
            connection.commit()
            connection.close()
        return result

    else:
        with connection.cursor() as c:

            textid = str(uuid.uuid4()).replace("-", "")

            c.execute(
                'INSERT INTO REST_entity'
                '(id, in_entity, type_entity, session_id) VALUES '
                '(%s, %s, %s, %s)',
                [textid, entity, entitytype, str(sessionid).replace("-", "")]
            )

            # print("-----------------------")
            connection.commit()
            connection.close()

        return result

def getentities(sessionid):
    connection = new_db_connection()
    with connection.cursor() as c:
        c.execute(
            'SELECT * FROM REST_entity '
            'WHERE session_id=%s ',
            [str(sessionid).replace("-", "")]
        )
        result = c.fetchall()
        connection.commit()
        connection.close()

    entities = []

    for entity in result:
        entities.append(dict(zip([column[0] for column in c.description], entity)))

    # print(entities)

    return entities

class de_identify(Process):

    def __init__(self, textdata, session):
        
        # self.models = models
        self.textdata: dict = textdata
        self.session: dict = session
        self.language: str = self.session["language"]
        self.entities: list = getentities(self.session["id"])
        self.model: str = ""
        self.modeltype: str = ""
        self.snomed_edition: str = ""
        self.snomed_version: str = ""
        super(de_identify, self).__init__()

    def run(self):

        """
        :returns None
        step 1: perform language recognition on the sentence and try to get the language from the database.
        step 2: perform NER and set entities in database.
        step 3: classify the entities and decide whether they should be anonimized in the output after C2R processing.
        step 4: anonimze the text with placeholders.
        """

        print("ts added")
        updatevalue("textdata", "time_start", str(self.textdata["id"]).replace("-", ""), float(datetime.datetime.now().timestamp()))

        # print("set language id")
        self.languageProcessor()
        # print(self.language)

        # print("detect entities")
        self.NERDetection()
        # print(self.entities)

        # print("classify entities")
        self.EntityClassification()
        # print(self.entities)

        # print("apply de-identitfy")
        self.NEApplier()
        # print(self.textdata["replacement_text"])

        updatevalue("textdata", "time_end", str(self.textdata["id"]).replace("-", ""), float(datetime.datetime.now().timestamp()))

    def languageProcessor(self):

        # Check if the language was already known
        if self.language is not None:
            language_code = self.session["language"]
        else:
            langid.set_languages(nermodels.keys())
            language_code, score = langid.classify(self.textdata["original_text"])

        # Set language in class
        self.language = language_code

        (self.model, self.modeltype, self.snomededition) = models[self.language]

        updatevalue("session", "language", self.session["id"], language_code)
        updatevalue("textdata", "status", self.textdata["id"], 2)

    def NERDetection(self):

        # Perform NER detection on sentence
        result_entities = nerPerformer(models[self.language], self.textdata["original_text"])

        # Store entities in database
        updatevalue("textdata", "entities", self.textdata["id"], json.dumps(result_entities))

        # Go over entities to store them seperately
        for entity in result_entities:
            addentity(entity, self.session["id"], result_entities[entity])
            # add created entity to class

        self.entities = getentities(self.session["id"])

        # Set status for sentence
        updatevalue("textdata", "status", self.textdata["id"], 3)

    def EntityClassification(self):

        # set base data for snomed connection
        baseUrl = 'https://browser.ihtsdotools.org/snowstorm/snomed-ct'
        # set edition to use using edition depending on language
        edition = self.snomed_edition
        # set version to use version set per language
        version = self.snomed_version

        # loop over entities found in the sentence
        for entity in self.entities:
            pass
            # url = baseUrl + '/browser/' + edition + '/' + version + '/concepts?term=' + entity.in_entity + '&activeFilter=true&offset=0&limit=50'
            #
            # response = requests.get(url)
            #
            # SIMDISTANCE = 0.85
            #
            # medical = False
            #
            # for result in response.json()["result"]:
            #     if entity in result["name"]:
            #         medical = True
            #     for term in result["name"].split(" "):
            #         if LIG3().sim(src=term, tar=entity) > SIMDISTANCE:
            #             medical = True
            #     else:
            #         medical = False
            #
            # if medical:
            #     entity.type_entity = "medical_domain"
            # else:
            #     pass

    def NEApplier(self):

        # if the enity is not an eponym of a disease

        for entity in self.entities:
            names = ["Mark", "Tom", "Erik", "Peter"]

            int = random.randint(0, 3)
            if entity["out_entity"] is None:
                updatevalue("entity", "out_entity", entity["id"], names[int])

        sentence = self.textdata["original_text"]

        self.entities = getentities(self.session["id"])

        for entity in self.entities:
            sentence = sentence.lower().replace(entity["in_entity"].lower(), entity["out_entity"].lower())

        updatevalue("textdata", "replacement_text", self.textdata["id"], sentence)

