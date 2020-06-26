from django.shortcuts import render,redirect
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to home page")