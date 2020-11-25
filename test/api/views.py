from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .form import LoginForm,RegisterForm
from test import urls
from django.template.loader import get_template

from .models import Postdb
#from djongo import models
import pymongo
import datetime

#from mongoengine import *
#from pymongo import Connections
#import mongoengine
# Create your views here.

# db = client.gettingStarted
# people = db.people


def input(request):
    context = {}
    x = request.GET.get('input')
    print(x)
    if x:
        context['input'] = x
        print(x)
    return render(request, 'input.html', context)


def post(request):
    context = {}
    x = request.POST.get('post')
    if x:
        context['post'] = x
    return render(request, 'post.html', context)


def form(request):
    context = {}
    x = request.POST.get('email')
    print(x)
    if x:
        context['form'] = x
    return render(request, 'form.html', {'form': LoginForm, 'form2': RegisterForm})
#    return HttpResponseRedirect('/input/')


def index(request):
    return HttpResponse("HI this is index")


def redirect(request):
    return HttpResponseRedirect('/input/')


def query(request):
    x = request.GET.get('input')
    print('1st')
    mypost = Postdb(name=x)
    print('2nd')
    mypost.save()
    print('3rd')
    print(Postdb.objects.all())
    print('after')
    #return 0
    return HttpResponseRedirect('/input/')
