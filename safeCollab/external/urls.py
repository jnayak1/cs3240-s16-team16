from django.conf.urls import include, url
from django.contrib import admin
from .views import login, logout, getReports

urlpatterns = [
    url(r'^(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<password>[a-zA-Z@\.\+\-\_]{0,30})$', login, name="login"),
    url(r'^logout/(?P<userkey>[A-Z0-9]{256})$', logout, name='logout'),
    url(r'^GetReports/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<userkey>[A-Z0-9]{256})$', getReports, name='getReports'),
]