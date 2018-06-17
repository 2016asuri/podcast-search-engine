# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from mygpoclient import simple, api, public, http
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests


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

    response2 = []

    #r = requests.get("http://gpodder.net/api/2/auth/%s/login.json".format(request.user.username))
    #client = api.MygPodderClient(request.user.username, request.user.password)
    client = simple.SimpleClient(request.user.username, request.user.password)
    #print request.user.password
    #client.update_device_settings('device_name', caption='My Device')
    subscriptions = []
    subscriptions.append('http://example.org/episodes.rss')
    subscriptions.append('http://example.com/feeds/podcast.xml')
    
    #sublist = client.get_subscriptions(None)

    device = api.PodcastDevice('manatee', 'My Device', 'mobile', 20)
    client.update_device_settings(device, caption='my device')
    client.put_subscriptions(device, subscriptions)
    

    try:
        #httpclient = http.HttpClient(request.user.username, request.user.password)
        #s = "http://gpodder.net/mygpoclient/subscriptions/%s.opml".format(request.user.username)
        #sublist = httpclient.GET(s)
        sublist = client.get_subscriptions(device)
    except http.NotFound:
        sublist = []
    for sub in sublist:
        response2.append(sub.title)
    return render(
    	request,
    	'newsfeed.html',
    	context = {'top25':response, 'sublist': response2},
    	)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('newsfeed')
        else: return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('newsfeed')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

    
#def subscriptions(request):
    
