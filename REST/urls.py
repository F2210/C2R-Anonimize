from django.urls import path, include
from REST.views import *


urlpatterns = [

    path('sessiondata', sessionEndpoint),
    path('sessiondata/<str:sessionID>/', sessionEndpoint),
    path('textdedata', textdataDeEndpoint),
    path('textdedata/<str:sentenceID>/', textdataDeEndpoint),
    path('textredata', textdataReEndpoint),
    path('textredata/<str:sentenceID>/', textdataReEndpoint),
]