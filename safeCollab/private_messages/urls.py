from django.conf.urls import patterns, url
from private_messages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	)
