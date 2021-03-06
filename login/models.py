from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class ActivateUser(models.Model):
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class DeactivateUser(models.Model):
    username = models.CharField(max_length = 50)

    def __str__(self):
        return self.username

class DeleteUser(models.Model):
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username




class Groupings(models.Model):
    name = models.CharField(max_length=50, unique=True)
    #name = models.ForeignKey(Group)
    members = models.ManyToManyField(User)
    def __str__(self):
        return (self.name, ", ".join(User.name for user in self.User.all()))

class SiteManager(models.Model):
    name = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):      #For Python 2, use __str__ on Python 3
        return self.title

class Report(models.Model):
    #reporter = models.ForeignKey(Reporter)
    description = models.CharField(max_length=128)
    detailed_description = models.CharField(max_length=255)
    public = models.BooleanField(default=0)
    tags = models.CharField(max_length=255)
    def __str__(self):
        return self.description

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name="user")
    public_key = models.CharField(max_length=512)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_images', blank=True)
    user_type = models.CharField(max_length=16)
    #Hold all of the groups the user belongs to
    groups = models.ManyToManyField(Group, related_name="groups")
    # public_key = models.CharField(max_length = 271)
    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
