from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
import django

from . import views

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^/$', views.index, name='index'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'$', views.index, name='index'),
]