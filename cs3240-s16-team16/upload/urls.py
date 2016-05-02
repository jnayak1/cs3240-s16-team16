from django.conf.urls import url

from upload.views import upload_file, uploaded, failed

urlpatterns = [
    #url(r'^$', home, name = 'homepage'),
    url(r'^$', upload_file, name = 'uploadpage'),
    url(r'^success/', uploaded, name = 'uploaded'),
    url(r'^failure/', failed, name = 'failed')
]