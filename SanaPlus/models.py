# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User,Permission

# Create your models here.

class relation_parent_user(models.Model):
    id=models.AutoField(primary_key=True,max_length=20)
    child = models.OneToOneField(User)
    parent = models.IntegerField()



class user_Token(models.Model):
    id=models.AutoField(primary_key=True,max_length=20)
    user_token = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48,unique=True)


    def __unicode__(self):
        return "{}_token".format(self.user_token)



class type_apps(models.Model):
    id=models.AutoField(primary_key=True, max_length=20)
    name=models.CharField(max_length=100)


class Apps_tokens_admin(models.Model):
    id=models.AutoField(primary_key=True,max_length=20)
    user_token = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48,unique=True)
    type_apps=models.ForeignKey(type_apps,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    date_create_apps=models.DateField()



    def __unicode__(self):
        return "{}_token".format(self.user_token)





class Events_Apps(models.Model):
    id=models.AutoField(primary_key=True,max_length=20)
    name=models.CharField(max_length=250)
    code=models.CharField(max_length=6, unique=True)
    descrip=models.TextField()
    date_create_Events = models.DateField()
    apps_events=models.ForeignKey(Apps_tokens_admin,on_delete=models.CASCADE)


class Happening_Events(models.Model):
    id=models.AutoField(primary_key=True)
    apps=models.ForeignKey(Apps_tokens_admin, on_delete=models.CASCADE)
    Events=models.ForeignKey(Events_Apps, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField()



