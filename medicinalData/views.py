from django.shortcuts import render, redirect
import csv
import pandas as pd
import os
from medicinalData.models import *
from django.http import HttpResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from pprint import pprint
import re
from datetime import datetime
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string


# Create your views here.
def add_medicines(request):
    os.chdir('/home/akash/healtholio/data')
    df = pd.read_csv('Medicines.csv')
    df = df['Medicines']
    for i in df:
        med = Medicine()
        med.name = i
        med.save()
    return HttpResponse("Added medicines")


def add_symptoms(request):
    os.chdir('/home/akash/healtholio/data')
    df = pd.read_csv('Symptoms.csv')
    df = df['Symptoms:']
    for i in df:
        sym = Symptom()
        sym.name = i
        sym.save()
    return HttpResponse("Added symptoms")


def add_diseases(request):
    os.chdir('/home/akash/healtholio/data')
    df = pd.read_csv('Diseases.csv')
    df = df['Diseases']
    for i in df:
        dis = Disease()
        dis.name = i
        dis.save()
    return HttpResponse("Added Diseases")


def getpdf(request):
    html = '<h1 color="red"> hello world </h1>'
    return HttpResponse("hello")


def docHome(request):
    return render(request, 'doctor_homepage.html')


def extractTranscript(request):
    sample = "Name Akash age 30 having symptoms cold, cough and nausea \
        is suffering from fever. He is prescribed tablet Advil 20 mg for \
        2 days to be taken at night after food, syrup Medrol for 3 days \
        to be taken in the morning before food. Advised not to eat outside food and not to eat cold food."
    #sample = request.POST['transcript']
    #
    # return HttpResponse("hello world")
    #sample = request.POST['final_text3']
    print('\n\n\n sample is :')
    print(sample)

    stopWords = stopwords.words('english')
    sampleVector = sent_tokenize(sample)
    sampleVector = word_tokenize(sample)
    sentence = [w.strip().strip()
                for w in sampleVector if w not in stopWords and w != '.']
    tagged = nltk.pos_tag(sentence)
    POS = [item[1] for item in tagged]
    # print (sentence)
    # print (tagged)
    # print (POS)
    Structured = {"Patient Name": "",
                  "Age": "",
                  "Gender": "",
                  "Symptoms": "",
                  "Disease": "",
                  "Medicines": "",
                  "Advice": ""
                  }

    if 'name' in sentence:
        ind = sentence.index('name')
    elif 'Name' in sentence:
        ind = sentence.index('Name')
    elif POS[0] == "NNP":
        ind = -1

    name = ""
    position = ind+1
    if POS[position] == "NNP":
        while POS[position] == "NNP":
            name += sentence[position]+" "
            position += 1
        Structured["Patient Name"] = name.strip()
        #print (name)

    else:
        print("Name not found")

    print("Extracted Name!")
    #pprint (Structured)

    if 'aged' in sentence:
        ind = sentence.index('aged')
        pos = ind+1
    elif 'age' in sentence:
        ind = sentence.index('age')
        pos = ind+1
    elif 'years' in sentence:
        pos = sentence.index('years')-1

    if POS[pos] == "CD":
        age = sentence[pos]
        #print (age)
        Structured['Age'] = age.strip()

    print("Extracted Age!")
    #pprint (Structured)

    if 'female' or 'Female' in sentence:
        Structured['Gender'] = "Female"
    elif 'male' or 'Male' in sentence:
        Structured['Gender'] = "Male"

    print("Extracted Gender!")
    #pprint (Structured)

    symptoms = []
    ind = sentence.index('symptoms')

    for i in range(ind+1, len(sentence)):
        slist = Symptom.objects.filter(name=sentence[i])
        if len(slist) == 1 and sentence[i] not in symptoms:
            symptoms.append(sentence[i])

    #print (symptoms)
    print("Extracted Symptoms!")
    Structured["Symptoms"] = ", ".join(symptoms)
    #pprint (Structured)

    disease = ''
    if "suffering from" in sample:
        ind = sentence.index("suffering")

    elif "diagonsed" in sample:
        ind = sentence.index("diagnosed")

    for i in range(ind+1, len(sentence)):
        dlist = Disease.objects.filter(name=sentence[i])
        if len(dlist) == 1:
            disease = sentence[i]

    Structured["Disease"] = disease
    #print (diseases)
    print("Extracted Diseases!")
    #pprint (Structured)

    med = []
    duration = []
    before_after = []
    day_night = []

    sample_list = word_tokenize(sample)

    for i in range(ind, len(sentence)):
        #print('med is :',sentence[i])

        mlist = Medicine.objects.filter(name__iexact=sentence[i])
        #print('mlist is :',mlist)

        if len(mlist) == 1 and POS[i] == "NNP":
            print('entered if')
            if sentence[i-1].lower() == "tablet":
                med.append(sentence[i-1][0].upper()+". " +
                           mlist[0].name+" "+sentence[i+1]+"mg")
            else:
                med.append(sentence[i-1][0].upper()+". "+mlist[0].name)
            print('med list is ', med)
        if sentence[i].isdigit() and sentence[i+1].lower() == "days" and POS[i] == "CD":
            duration.append(sentence[i]+" "+sentence[i+1])

    for i in range(len(med)):
        ind = sample_list.index(med[i].split(' ')[1])
        ind_daynight = ind

        foundDayNight = False
        while foundDayNight == False and ind_daynight <= len(sample_list):
            if sample_list[ind_daynight].lower() in ["night", "afternoon", "evening", "morning"]:
                foundDayNight = True
                day_night.append(sample_list[ind_daynight])
            ind_daynight += 1

        foundBeforeAfter = False
        ind_beforeafter = ind

        while foundBeforeAfter == False and ind_beforeafter <= len(sample_list):
            if sample_list[ind_beforeafter].lower() in ["before", "after"]:
                foundBeforeAfter = True
                before_after.append(sample_list[ind_beforeafter]+" food")
            ind_beforeafter += 1

    med_data = []
    d = {"At": "", "Medicine_Name": "", "Taken": "", "Duration": ""}
    for i in range(len(med)):
        d["Medicine_Name"] = med[i]
        d["At"] = day_night[i]
        d["Taken"] = before_after[i]
        d["Duration"] = duration[i]
        med_data.append(d)
        d = {}

    Structured["Medicines"] = med_data
    #print (sample_list[ind_daynight])

    # pgm#$%cdac VITC-PGM

    sample_list = nltk.word_tokenize(sample)

    if "advices" in sample_list:
        ind = sample_list.index("advices")
    elif "advice" in sample_list:
        ind = sample_list.index("advice")
    elif "advise" in sample_list:
        ind = sample_list.index("advise")
    elif "advised" in sample_list:
        ind = sample_list.index("advised")
    elif "adviced" in sample_list:
        ind = sample_list.index("adviced")
    elif "Advices" in sample_list:
        ind = sample_list.index("Advices")
    elif "Advice" in sample_list:
        ind = sample_list.index("Advice")
    elif "Advise" in sample_list:
        ind = sample_list.index("Advise")
    elif "Advised" in sample_list:
        ind = sample_list.index("Advised")
    elif "Adviced" in sample_list:
        ind = sample_list.index("Adviced")

    notes = (" ".join(sample_list[ind+1:len(sample_list)])).split(",")
    for i in range(len(notes)):
        notes[i] = notes[i].strip()
        notes[i] = notes[i][0].upper()+notes[i][1:]

    Structured['Advice'] = ','.join(notes)
    print("Extracted Advice!")
    patient = user.objects.get(id=int(request.POST['pid']))
    doctor = request.user
    Structured['patient'] = patient
    Structured['doctor'] = doctor
    pprint(Structured)
    return render(request, 'prescription.html', Structured)


def getTemplate(p1):
    l1 = linktable.objects.filter(prescription=p1).filter(
        user__type__iexact="patient")[0]
    l2 = linktable.objects.filter(prescription=p1).filter(
        user__type__iexact="doctor")[0]
    doc = l2.user
    patient = l1.user
    dosage_list = Dosage.objects.filter(prescription=p1)
    symptom_list = complaints.objects.filter(prescription=p1)
    advice_list = Advice.objects.filter(prescription=p1)
    med_data = []
    Structured = {}

    Structured["Disease"] = p1.diagnosis.name

    for i in dosage_list:
        d = {"At": "", "Medicine_Name": "", "Taken": "", "Duration": ""}
        amount = i.amount or ''
        type = i.med_type
        d["Medicine_Name"] = type + ' ' + i.med.name + ' ' + amount
        d["At"] = i.time_of_day
        d["Taken"] = i.when
        d["Duration"] = i.duration
        med_data.append(d)
        d = {}
    Structured['Medicines'] = med_data

    notes = []
    for i in advice_list:
        notes.append(i.adv)
    Structured['Advice'] = ','.join(notes)

    coms = []
    for i in symptom_list:
        coms.append(i.symptom.name)
    Structured["Symptoms"] = ", ".join(coms)

    Structured['patient'] = patient
    Structured['doctor'] = doc

    return Structured


def verified(request):
    p1 = Prescription()
    dis = Disease.objects.get(name=request.POST['disease'])
    p1.diagnosis = dis
    p1.save()
    l1 = linktable()
    l1.prescription = p1
    l1.user = request.user
    l1.save()
    u2 = user.objects.get(id=int(request.POST['pid']))
    l2 = linktable()
    l2.prescription = p1
    l2.user = u2
    l2.save()
    #mlist =[]
    i = 1
    flag = True
    while flag:
        try:
            meds = request.POST['drug'+str(i)].split(' ')
            mname = meds[1]
            print('mname is ', mname)
            m1 = Medicine.objects.get(name=mname)
            Dos = Dosage()
            Dos.time_of_day = request.POST['time_of_day' + str(i)]
            Dos.duration = request.POST['duration' + str(i)]
            Dos.when = request.POST['when' + str(i)]
            Dos.med = m1
            Dos.prescription = p1
            Dos.med_type = meds[0]
            try:
                Dos.amount = meds[2]
            except IndexError:
                pass
            Dos.save()
            i += 1
        except KeyError:
            flag = False
    symps = request.POST['symptoms'].split(',')
    for i in symps:
        s1 = Symptom.objects.get(name=i.strip())
        com = complaints()
        com.symptom = s1
        com.prescription = p1
        com.save()

    advices = request.POST['note'].split(',')
    for i in advices:
        ad = Advice()
        ad.adv = i
        ad.prescription = p1
        ad.save()

    print('all saved')
    context = getTemplate(p1)
    mail_body = render_to_string('prescription.html', context)
    send_email(u2, mail_body)
    return redirect('/home/doctor')


def send_email(user, body):
    subject = 'Your digital prescription'
    html_content = body
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['maravind2000@gmail.com']
    text_content = 'Hello ' + user.name
    # send_mail( subject, message, email_from, recipient_list )
    # print("mail send")
    #

    # email = EmailMessage(subject, body=message,
    #                      from_email=email_from, to=recipient_list)
    # os.chdir('/home/akash/healtholio/data/')
    # email.attach_file('Symptoms.csv')
    # email.send()
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('email sent')

def getCurrentPres(request):
    pass