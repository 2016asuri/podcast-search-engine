from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^newsfeed$', views.newsfeed, name='newsfeed'),
    url('^login/$', views.login, name='login'),
    url('^signup/$', views.signup, name='signup'),
]