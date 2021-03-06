from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search),
    url(r'^(?P<reportID>\w{0,50})/$', views.getReport),
    url(r'^(?P<reportID>\w{0,50})/togglePrivate/$', views.togglePrivate),
    url(r'^(?P<reportID>\w{0,50})/deleteReport/$', views.deleteReport),
    url(r'^folder/(?P<folderID>\w{0,50})/$', views.getFolder)
)
