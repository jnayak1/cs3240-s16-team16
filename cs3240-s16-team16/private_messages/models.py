from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey(User)
	content = models.BinaryField()
	encrypted = models.BooleanField(default=False)

class ConversationLog(models.Model):
	participants = models.ManyToManyField(User)
	log = models.ManyToManyField(Message)
	readBy = models.ManyToManyField(User, related_name="readBy")