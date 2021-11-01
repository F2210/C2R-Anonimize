from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from REST.models import *
import json
from multiprocessing import Process
from Anonimize.controller import Anonimize
# Create your views here.

@csrf_exempt
def sessionEndpoint(request, sessionID=None):
    """
    Data input by C2R to start a Anonimization session.

    :param request: request.body: {
        "sessionID": 1,
        "clientID": 1,
        "clientData": {
            "firstname": "",
            "lastname": "",
            "address": "",
            "nation": "",
            "birthdate": "",
        "caregiverID": 1,
        "caregiverData": {
            "firstname": "",
            "lastname": "",
            "address": "",
            "nation": "",
            "birthdate": "",
        }
    }
    :return: {
        "sessionID": 0001,
        "clientID": 0001,
        "status": 1
    }
    """

    global returndata

    if request.method == "GET":

        try:
            session = Session.objects.get(
                identifier=sessionID
            )

            sentences = Sentence.objects.filter(session=session)

            returnsentences = []
            replacement_returntext = ""
            original_returntext = ""

            for sentence in sentences:
                returnsentences.append({
                    "original": sentence.original_text,
                    "replaced": sentence.replacement_text,
                    "entities": sentence.entities,
                })
                replacement_returntext += sentence.replacement_text + ". "
                original_returntext += sentence.original_text + ". "

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "sessionID": session.identifier,
                    "clientID": session.client.id,
                    "caregiverID": session.caregiver.id,
                    "original_text": original_returntext,
                    "anonimzed_text": replacement_returntext,
                    "anonimization_details": returnsentences,
                }
            }

        except Session.DoesNotExist:

            returndata = {
                "status_code": 404,
                "response": "failed",
                "response_data": {
                    "error": "Session not found."
                }
            }

    elif request.method == "POST":

        requesttype = request.GET

        if requesttype["type"] == "open":

            data = json.loads(request.body)

            client = Client.objects.get_or_create(
                client_id=data["clientID"]
            )

            if client[1]:
                client[0].data = data["clientData"]
                client[0].save()

            caregiver = Caregiver.objects.get_or_create(
                caregiver_id=data["caregiverID"]
            )

            if caregiver[1]:
                caregiver[0].data=data["caregiverData"]
                caregiver[0].save()

            session = Session.objects.create(
                identifier=data["sessionID"],
                client=client[0],
                caregiver=caregiver[0],
                status=0
            )

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "sessionID": session.identifier,
                    "clientID": session.caregiver.id,
                    "caregiverID": session.client.id,
                    "session_status": session.status
                }
            }

        elif requesttype["type"] == "close":

            data = json.loads(request.body)

            session = Session.objects.get(
                identifier=data["sessionID"],
            )

            if session.status == 0:

                sentences = Sentence.objects.filter(session=session)

                returnsentences = []
                replacement_returntext = ""
                original_returntext = ""

                for sentence in sentences:
                    returnsentences.append({
                        "original": sentence.original_text,
                        "replaced": sentence.replacement_text,
                        "entities": sentence.entities,
                    })
                    replacement_returntext += sentence.replacement_text + ". "
                    original_returntext += sentence.original_text + ". "

                returndata = {
                    "status_code": 200,
                    "response": "success",
                    "response_data": {
                        "sessionID": session.identifier,
                        "clientID": session.client.id,
                        "caregiverID": session.caregiver.id,
                        "original_text": original_returntext,
                        "anonimzed_text": replacement_returntext,
                        "anonimization_details": returnsentences,
                    }
                }

                session.status = 1
                session.save()

            else:
                returndata = {
                    "status_code": 500,
                    "response": "failed",
                    "response_data": {
                        "error": "This session has already been closed. To parse closed session information use a GET request."
                    }
                }

    else:

        returndata = {
            "status_code": 500,
            "response": "failed",
            "response_data": {
                "error": "No method was found to support this request."
            }
        }

    return JsonResponse(returndata, status=returndata["status_code"])

@csrf_exempt
def sentenceEndpoint(request, sentenceID=None):
    """

    :param request:
    :return:
    """

    if request.method == "GET":

        sentence = Sentence.objects.get(id=sentenceID)

        returndata = {
            "status_code": 200,
            "response": "success",
            "response_data": {
                "sentenceID": sentence.pk,
                "original_text": sentence.original_text,
                "anonimized_text": sentence.replacement_text,
                "entities": sentence.entities,
                "sessionID": sentence.session.id,
                "status": sentence.status
            }
        }

    elif request.method == "POST":

        data = json.loads(request.body)

        try:
            session = Session.objects.get(identifier=data["sessionID"])

            sentence = Sentence.objects.create(
                original_text=data["text"],
                session=session
            )

            client = session.client
            caregiver = session.caregiver

            processingdata = (session, sentence, client, caregiver)

            process = Anonimize(sentence, session, client, caregiver)
            process.daemon = True
            process.start()

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "sentenceID": sentence.pk,
                    "sentenceText": sentence.original_text,
                    "status": sentence.status
                }
            }
        except Session.DoesNotExist:
            returndata = {
                "status_code": 404,
                "response": "failed",
                "response_data": {
                    "error": "Session not found."
                }
            }
    else:
        returndata = {
            "status_code": 500,
            "response": "failed",
            "response_data": {
                "error": "No method was found to support this request."
            }
        }

    return JsonResponse(returndata, status=returndata["status_code"])