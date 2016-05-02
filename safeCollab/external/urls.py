from django.conf.urls import include, url
from django.contrib import admin
from .views import login, logout, getReports, verifyUser, receiveFile, seeReport, getFile

urlpatterns = [
    url(r'^(?P<username>[a-zA-Z0-9@\.\+\-\_\;\,\:\?\>\<\\\[\]\{\}\|]{0,30})/(?P<password>[a-zA-Z0-9@\.\+\-\_\;\,\:\?\>\<\\\[\]\{\}\|]{0,30})$', login, name="login"),
    url(r'^logout/(?P<userkey>[A-Z0-9]{256})$', logout, name='logout'),
    #Get the names of the reports the user can see
    url(r'^GetReports/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<userkey>[A-Z0-9]{256})$', getReports, name='getReports'),
    #Verify that the user has an active session and is still a user
    url(r'^verifyUser/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<userkey>[A-Z0-9]{256})$', verifyUser, name='verifyUser'),
    #Handle uploading files
    url(r'^receiveFile/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<userkey>[A-Z0-9]{256})/(?P<file_name>[0-9a-zA-Z@\.\+\-\_]{0,260})/(?P<encrypted>((True)|(False)))$', receiveFile, name='receiveFile'),
    #See the requested report
    url(r'^seeReport/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<report_name>[a-zA-Z0-9@\.\+\-\_" "]{0,50})$', seeReport, name='seeReport'),
    #Get the requested file
    url(r'^getFile/(?P<username>[a-zA-Z@\.\+\-\_]{0,30})/(?P<file_name>[0-9a-zA-Z0-9@\.\+\-\_\-" "]{0,50})$', getFile, name='getFile'),
]