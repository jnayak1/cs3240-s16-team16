from django.conf.urls import patterns, url
from private_messages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new_conversation/$', views.newConversation),
    url(r'^(?P<conversationID>\w{0,50})/$', views.getConversation),
	)
