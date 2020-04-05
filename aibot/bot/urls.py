from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^post/$', views.Post, name='post'),
]
