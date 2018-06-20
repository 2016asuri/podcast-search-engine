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
from lxml import html
from forms import ProfileForm
from models import Profile

client = None

def cmp_num_episodes(pod1, pod2):
    page1 = requests.get(pod1.mygpo_link)
    tree1 = html.fromstring(page1.content)
    episodes1 = tree1.xpath('//span[@class="released"][1]')
    page2 = requests.get(pod2.mygpo_link)
    tree2 = html.fromstring(page2.content)
    episodes2 = tree2.xpath('//span[@class="released"][1]')
    return len(episodes2)-len(episodes1)


def index(request):
    django.contrib.auth.logout(request)
    return render(request, 'index.html',)

def newsfeed(request):
    response = []
    devices = client.get_devices()
    device = None
    for d in devices:
        if d.device_id==request.user.profile.device_id: device = d

    subscriptions = []

    public_client = public.PublicClient()
    toplist = public_client.get_toplist()
    for index, entry in enumerate(toplist):
        response.append( (entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]) )
        subscriptions.append(entry.url)

    response2 = []
    errors = []
    
    try:
        sublist = client.get_subscriptions(device)
    except http.NotFound: #device does not exist
        errors.append('Device does not exist or you are not a registered user with gPodder.net.')
        response2 = []
        sublist = []

    if device == None:
        print 'error'
        if len(errors)==0: errors.append('Device does not exist or you are not a registered user with gPodder.net.')
        response2 = []
        sublist = []

    for i in range(len(sublist)):
        entry = public_client.get_podcast_data(sublist[i])
        sublist[i] = entry


    #sublist.sort(cmp_num_episodes)
    for index, entry in enumerate(sublist):
        response2.append( (entry.logo_url, entry.url, ['%s' % (entry.title), entry.description]))
        


    return render(
    	request,
    	'newsfeed.html',
    	context = {'sublist': response2, 'errors': errors},
    	)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            form2 = ProfileForm(data=request.POST, instance=request.user.profile)
            form2.save()
            if form2.is_valid():
                global client
                client = api.MygPodderClient(username, raw_password)
                
                return redirect('newsfeed')
        else: return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        form2 = ProfileForm()
    return render(request, 'login.html', {'form': form, 'form2':form2})

    
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
        pods.append(tag_resp)
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


