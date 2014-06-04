from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=20, default='', blank=True, null=True)
    desc = models.TextField(blank=True, null=True, default='')
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)
    proPic = models.ImageField(upload_to="%Y/%m/%d", default="")


class Plan(models.Model):
    arrTime = models.DateTimeField()
    title = models.CharField(max_length=60, default="")
    usr = models.ForeignKey(User,related_name='plan', null=True)
    des = models.CharField(max_length=30, default="")
    flightNr = models.CharField(max_length=20)
    desc = models.TextField(blank=True, null=True, default='')

class Activity(models.Model):
    plan = models.ForeignKey(Plan, related_name='activity')
    actTime = models.DateTimeField()
    actTitle = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True,default='')

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos')
    image = models.ImageField(upload_to="%Y/%m/%d")
