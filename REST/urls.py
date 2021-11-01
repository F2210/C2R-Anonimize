from django.urls import path, include
from REST.views import *


urlpatterns = [

    path('sessiondata', sessionEndpoint),
    path('sessiondata/<str:sessionID>', sessionEndpoint),
    path('sentencedata', sentenceEndpoint),
    path('sentencedata/<int:sentenceID>', sentenceEndpoint),

]