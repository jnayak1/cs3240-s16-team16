from django.db import models

# Create your models here.
class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

class PublicKey(models.Model):
    file = models.CharField(max_length=50)
    key = models.CharField(max_length=32)

    def __str__(self):
        return self.file

# class UploadFile(models.Model):
#     name = models.CharField(max_length=120, blank=True)
#     file = models.FileField()
#
#     def __str__(self):
#         return self.name
