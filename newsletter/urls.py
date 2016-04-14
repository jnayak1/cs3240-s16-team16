from django.conf.urls import include, url
from django.contrib import admin
from newsletter.views import home, upload_file, uploaded, failed

urlpatterns = [
    #url(r'^$', home, name = 'homepage'),
    url(r'^$', upload_file, name = 'uploadpage'),
    url(r'^success/', uploaded, name = 'uploaded'),
    url(r'^failure/', failed, name = 'failed')
]