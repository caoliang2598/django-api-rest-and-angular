from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=20, default="")
    desc = models.CharField(max_length=100,default="")
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)
    proPic = models.ImageField(upload_to="%Y/%m/%d", default="")


class Plan(models.Model):
    time = models.DateTimeField()
    usr = models.ForeignKey(User,related_name='plan')
    des = models.CharField(max_length=50)
    dur = models.PositiveIntegerField(default=0)
    flightNr = models.CharField(max_length=20)



class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos')
    image = models.ImageField(upload_to="%Y/%m/%d")
