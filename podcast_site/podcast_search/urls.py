from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newsfeed$', views.newsfeed, name='newsfeed'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^genres/$', views.genres, name='genres'),
]