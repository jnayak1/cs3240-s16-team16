from django.contrib import admin

# Register your models here.
from .models import Tracker

class TrackerAdmin(admin.ModelAdmin):
    list_display = ['username', 'key']
    class Meta:
       model = Tracker

admin.site.register(Tracker, TrackerAdmin)