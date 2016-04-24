from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

class File(models.Model):
	title = models.CharField(max_length=50)
	publisher = models.ForeignKey(User)
	timeStamp = models.DateTimeField(auto_now=True)
	content = models.FileField(upload_to='files')

class Folder(models.Model):
	owner = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	parentFolder = models.ForeignKey('self', blank=True, null=True)
	reports = models.ManyToManyField('Report', blank=True)

class Report(models.Model):
	title = models.CharField(max_length=50)
	shortDescription = models.TextField(max_length=160)
	longDescription = models.TextField()
	timeStamp = models.DateTimeField(auto_now=True)
	files = models.ManyToManyField(File, blank=True)
	private = models.BooleanField(default=True)
# 	group = models.ForeignKey(Group, related_name='group', null = True)
# 	parentFolder = models.ForeignKey(Folder)
	group = models.ForeignKey(Group, related_name='group')
	owner = models.ForeignKey(User, related_name="reporter")
	collaborators = models.ManyToManyField(User, max_length=160)

	@classmethod
	def create(self, owner, title, parentFolder, group):
		return self(owner=owner, title=title, parentFolder=parentFolder,
			shortDescription="Write a short description",
			longDescription="Write a longer description",
			group=group)

	def __str__(self):
		return self.title + str(self.group)
