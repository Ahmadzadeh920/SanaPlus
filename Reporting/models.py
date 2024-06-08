# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import unicode_literals
from django.contrib import admin

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User,Permission
from SanaPlus.models import Events_Apps ,Apps_tokens_admin




class Record_Events(models.Model):
    id = models.AutoField(primary_key=True)
    json_fields = JSONField()
    date_record = models.DateTimeField()
    Event_id = models.IntegerField()




class PageRank(models.Model):
    id=models.AutoField(primary_key=True)
    Event_id = models.IntegerField()
    date_record = models.DateTimeField()
    json_fields = JSONField() # must be included title , urls , referrer


class Reserve(models.Model):
    id=models.AutoField(primary_key=True)
    Event_id=models.IntegerField()
    date_record = models.DateTimeField()
    json_fields=JSONField()# must be included product , IP , session_id , user , Reservastion_id
    Reservation_id = models.IntegerField()



class Sell(models.Model):
    id=models.AutoField(primary_key=True)
    Event_id = models.IntegerField()
    date_record = models.DateTimeField()
    json_fields=JSONField() # must be included product , IP , session_id , user , Reservastion_id , Price
    Reservation_id=models.IntegerField()

class visited_Product(models.Model):
    id= models.AutoField(primary_key=True)
    Event_id=models.IntegerField()
    json_fields = JSONField() #must be included product , IP , session_id , user
    date_record = models.DateTimeField()

class Search_Product(models.Model):
    id = models.AutoField(primary_key=True)
    Event_id = models.IntegerField()
    json_fields = JSONField()# must be included product , IP , session_id , user
    date_record = models.DateTimeField()

class Register_user(models.Model):
    id = models.AutoField(primary_key=True)
    Event_id = models.IntegerField()
    json_fields = JSONField() #must be included  IP , session_id , user
    date_record = models.DateTimeField()

