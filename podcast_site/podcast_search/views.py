# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from mygpoclient import simple, api, public
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return render(request, 'index.html',)

# Create your views here.

def newsfeed(request):
    response = []

    client = public.PublicClient()
    toplist = client.get_toplist()
    for index, entry in enumerate(toplist):
        response.append( '%4d. %s' % (index+1, entry.title) )

    #return HttpResponse(response)
    return render(
    	request,
    	'newsfeed.html',
    	context = {'top25':response},
    	)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #return HttpResponse(request)
            return render(request, 'index.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #return HttpResponse(request)
            return render(request, 'index.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})

    