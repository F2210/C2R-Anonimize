from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from REST.models import *
import json
from transformers import AutoTokenizer
from multiprocessing import Process
from Anonimize.controller import de_identify
# Create your views here.

@csrf_exempt
def sessionEndpoint(request, sessionID=None):
    """
    Data input by C2R to start a Anonimization session.

    :param request: request.body: {
        "sessionID": 1,
    }
    :return: {
        "sessionID": 0001,
        "status": 1
    }
    """

    global returndata

    if request.method == "GET":

        try:
            session = Session.objects.get(Q(identifier=sessionID) | Q(id=sessionID))

            textdata = TextData.objects.filter(session=session)

            returntextdata = []
            replacement_returntext = ""
            original_returntext = ""

            errorsentences: set = set({})

            for textdata in textdata:
                returntextdata.append({
                    "original": textdata.original_text,
                    "replaced": textdata.replacement_text,
                    "entities": textdata.entities,
                })
                try:
                    replacement_returntext += textdata.replacement_text.strip() + " "
                except:
                    replacement_returntext += "ERROR {'sentence': '" + str(textdata.pk) + "'}"
                    errorsentences.add(textdata.pk)
                try:
                    original_returntext += textdata.original_text.strip() + " "
                except:
                    original_returntext += "ERROR {'sentence': '" + str(textdata.pk) + "'}"
                    errorsentences.add(textdata.pk)

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "ID": session.id,
                    "customID": session.identifier,
                    "original_text": original_returntext,
                    "anonimzed_text": replacement_returntext,
                    "anonimization_details": returntextdata,
                    "errorsentences": list(errorsentences),
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

            session = Session.objects.get_or_create(
                identifier=data["sessionID"],
            )

            session = session[0]

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "ID": session.id,
                    "customID": session.identifier,
                    "session_status": session.status
                }
            }

        elif requesttype["type"] == "close":

            data = json.loads(request.body)

            session = Session.objects.get(
                identifier=data["sessionID"],
            )

            if session.status == 0:

                textdata = TextData.objects.filter(session=session)

                returntextdata = []
                replacement_returntext = ""
                original_returntext = ""

                for textdata in textdata:
                    returntextdata.append({
                        "original": textdata.original_text,
                        "replaced": textdata.replacement_text,
                        "entities": textdata.entities,
                    })
                    replacement_returntext += textdata.replacement_text
                    original_returntext += textdata.original_text

                returndata = {
                    "status_code": 200,
                    "response": "success",
                    "response_data": {
                        "ID": session.id,
                        "customID": session.identifier,
                        "original_text": original_returntext,
                        "anonimzed_text": replacement_returntext,
                        "anonimization_details": returntextdata,
                    }
                }

                session.delete()

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
def textdataDeEndpoint(request, textdataID=None):
    """

    :param request:
    :return:
    """

    if request.method == "GET":

        textdata = TextData.objects.get(id=textdataID)

        returndata = {
            "status_code": 200,
            "response": "success",
            "response_data": {
                "textdataID": textdata.pk,
                "original_text": textdata.original_text,
                "anonimized_text": textdata.replacement_text,
                "entities": textdata.entities,
                "sessionID": textdata.session.id,
                "status": textdata.status
            }
        }

    elif request.method == "POST":

        data = json.loads(request.body)

        try:
            sessiondbobj = Session.objects.get(id=data["sessionID"])

            textdbobj = TextData.objects.create(
                original_text=data["text"],
                session=sessiondbobj,
                type=False
            )

            textdata = {
                "id": textdbobj.pk,
                "original_text": data["text"],
                "sessionid": textdbobj.session.pk,
            }

            session = {
                "id": sessiondbobj.pk,
                "language": sessiondbobj.language
            }

            print("starting processing")
            process = de_identify(textdata, session)
            process.daemon = True
            process.start()

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "textdataID": textdbobj.pk,
                    "textdataText": textdbobj.original_text,
                    "status": textdbobj.status
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

@csrf_exempt
def textTokenizer(request):

    if request.method == "POST":

        data = request.POST

        print(data)

        tokenizer = AutoTokenizer.from_pretrained("wietsedv/bert-base-dutch-cased-finetuned-sonar-ner")

        print(tokenizer(data["sentence"]).decode())

@csrf_exempt
def textdataReEndpoint(request, textdataID=None):
    """

    :param request:
    :return:
    """

    if request.method == "GET":

        textdata = TextData.objects.get(id=textdataID)

        returndata = {
            "status_code": 200,
            "response": "success",
            "response_data": {
                "textdataID": textdata.pk,
                "original_text": textdata.original_text,
                "anonimized_text": textdata.replacement_text,
                "entities": textdata.entities,
                "sessionID": textdata.session.id,
                "status": textdata.status
            }
        }

    elif request.method == "POST":

        data = json.loads(request.body)

        try:
            session = Session.objects.get(id=data["sessionID"])

            textdata = TextData.objects.create(
                original_text=data["text"],
                session=session,
                type=True
            )

            process = de_identify(textdata, session)
            process.daemon = True
            process.start()

            returndata = {
                "status_code": 200,
                "response": "success",
                "response_data": {
                    "textdataID": textdata.pk,
                    "textdataText": textdata.original_text,
                    "status": textdata.status
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