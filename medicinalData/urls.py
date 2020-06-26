from django.urls import path,re_path
from .views import add_diseases,add_medicines,add_symptoms,extractTranscript,docHome,send_email,verified

urlpatterns = [
    re_path(r'^data/add/medicine',add_medicines),
    re_path(r'^data/add/disease',add_diseases),
    re_path(r'^data/add/symptom',add_symptoms),
    re_path(r'^extract',extractTranscript),
    re_path(r'^home/doctor',docHome),
    re_path(r'^email/',send_email),
    re_path(r'^verify/',verified),
]
