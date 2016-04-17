from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<reportID>\w{0,50})/$', views.getReport),
    url(r'^folder/(?P<folderID>\w{0,50})/$', views.getFolder)
	)
