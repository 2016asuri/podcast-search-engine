# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from mygpoclient import simple, api, public, http, locator, feeds
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests, django


client = None
def index(request):
    django.contrib.auth.logout(request)
    return render(request, 'index.html',)

# Create your views here.

def newsfeed(request):
    response = []
    #client = api.MygPodderClient('2016asuri', 'Febru@ry98')
    device = api.PodcastDevice('device', 'Device', 'desktop', 0) #will have to add device to login form
    subscriptions = []

    public_client = public.PublicClient()
    toplist = public_client.get_toplist()
    for index, entry in enumerate(toplist):
        response.append( (entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]) )
        subscriptions.append(entry.url)



    response2 = []

    #client = api.MygPodderClient(request.user.username, client_password)
    
    #
    #subscriptions.append('http://feeds.feedburner.com/linuxoutlaws')
    #subscriptions.append('http://example.com/feeds/podcast.xml')

    client.put_subscriptions(device, subscriptions)
    
    #if client_password == '': return render(request, 'index.html')
    try:
        sublist = client.get_subscriptions(device)
    except http.NotFound: #device does not exist
        sublist = ['You are not a registered gPodder user. Please register at gPodder.net.']
    for index, uri in enumerate(sublist):
        entry = public_client.get_podcast_data(uri)
        response2.append( (entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]))

    #locator = simple.SimpleClient('2016asuri', 'Febru@ry98').locator
    #r = locator.download_episode_actions_uri(podcast='http://feeds.feedburner.com/linuxoutlaws')
    #print requests.get(r)
    #r = requests.get('http://gpodder.net/api/2/episodes/2016asuri.json http://feeds.feedburner.com/linuxoutlaws')
    #print r.text
    #print public_client.get_episode_data('http://feeds.feedburner.com/linuxoutlaws')
    #r = client.download_episode_actions(None)
    
    #print r.actions
    #uri = 'http://feeds.feedburner.com/linuxoutlaws'
    #p = public_client.get_podcast_data(uri)
    #print p.mygpo_link
    #print(public_client.get_episode_data(uri, )) 

    #feed = get_feed(uri) 
    #print feed
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
            #client_password = raw_password
            global client
            client = api.MygPodderClient(username, raw_password)
            print(client)
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
        tag_pods = public_client.get_podcasts_of_a_tag(tag)
        tag_pods = list(set(tag_pods))
        for index, entry in enumerate(tag_pods):
            tag_resp.append((entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]))
        #tag_resp = list(set(tag_resp))
        pods.append(tag_resp)
  #  return render(request, 'genres.html', {'tags':toptags, 'pods':response, 'tag_nums':range(10), 'pod_nums':range(50)})
    tags = [tag.capitalize() for tag in tags]
    return render(request, 
    'genres.html',
    {'tag0': tags[0], 'tag1': tags[1], 'tag2': tags[2], 'tag3': tags[3], 'tag4': tags[4],
    'tag5': tags[5], 'tag6': tags[6], 'tag7': tags[7], 'tag8': tags[8], 'tag9': tags[9], 
    'pods0': pods[0], 'pods1': pods[1], 'pods2': pods[2], 'pods3': pods[3], 'pods4': pods[4],
    'pods5': pods[5], 'pods6': pods[6], 'pods7': pods[7], 'pods8': pods[8], 'pods9': pods[9], })

def logout(request):
    return index(request)

def search(request):
    if request.method == 'POST':
        print request.POST
        search_term = request.POST['search_term']
        client = public.PublicClient()
        pods = []
        for entry in client.search_podcasts(search_term):
            pods.append((entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]))
        pods = list(set(pods))
        return render(request, 'search.html', {'heading': 'Your results:', 'pods': pods})   
    return render(request, 'search.html')


