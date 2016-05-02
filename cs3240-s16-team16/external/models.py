from django.db import models

# Create your models here.
class Tracker(models.Model):
    username = models.CharField(max_length=30)
    key = models.CharField(max_length=256)

    def __str__(self):
        return self.key