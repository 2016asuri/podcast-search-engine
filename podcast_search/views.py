# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from mygpoclient import simple, api, public, http, locator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests


client_password = ''
def index(request):
    return render(request, 'index.html',)

# Create your views here.

def newsfeed(request):
    response = []

    public_client = public.PublicClient()
    toplist = public_client.get_toplist()
    for index, entry in enumerate(toplist):
        response.append( '%4d. %s' % (index+1, entry.title) )


    response2 = []

    #client = api.MygPodderClient(request.user.username, client_password)
    client = api.MygPodderClient('2016asuri', 'Febru@ry98')
    #subscriptions = []
    #subscriptions.append('http://example.org/episodes.rss')
    #subscriptions.append('http://example.com/feeds/podcast.xml')

    device = api.PodcastDevice('device', 'Device', 'desktop', 0) #will have to add device to login form
    
    #if client_password == '': return render(request, 'index.html')
    try:
        sublist = client.get_subscriptions(device)
    except http.NotFound: #device does not exist
        sublist = ['You are not a registered gPodder user. Please register at gPodder.net.']
    for index, entry in enumerate(sublist):
        response2.append( '%4d. %s' % (index+1, entry) )
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
            client_password = raw_password
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

    
def genres(request):
    public_client = public.PublicClient()
    toptags = public_client.get_toptags(10)
    tags = [tag.tag for tag in toptags]
    pods = []
    for tag in tags:
        tag_resp = []
        for index, pod in enumerate(public_client.get_podcasts_of_a_tag(tag)):
            tag_resp.append('%4d. %s' % (index+1, pod.title))
        pods.append(tag_resp)
  #  return render(request, 'genres.html', {'tags':toptags, 'pods':response, 'tag_nums':range(10), 'pod_nums':range(50)})
    return render(request, 
    'genres.html',
    {'tag0': tags[0], 'tag1': tags[1], 'tag2': tags[2], 'tag3': tags[3], 'tag4': tags[4],
    'tag5': tags[5], 'tag6': tags[6], 'tag7': tags[7], 'tag8': tags[8], 'tag9': tags[9], 
    'pods0': pods[0], 'pods1': pods[1], 'pods2': pods[2], 'pods3': pods[3], 'pods4': pods[4],
    'pods5': pods[5], 'pods6': pods[6], 'pods7': pods[7], 'pods8': pods[8], 'pods9': pods[9], })

def logout(request):
    django.contrib.auth.logout(request)
    return index(request)

def search(request):
    if request.method == 'POST':
        print request.POST
        search_term = request.POST['search_term']
        client = public.PublicClient()
        pods = []
        for pod in client.search_podcasts(search_term):
            pods.append(pod.title)
        return render(request, 'search.html', {'heading': 'Your results:', 'pods': pods})   
    return render(request, 'search.html')


