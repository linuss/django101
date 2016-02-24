from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now=True)
    photo = models.ImageField()

class Comment(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True)
