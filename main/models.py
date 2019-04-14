# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmailToken(models.Model):
    email = models.CharField(max_length = 100, primary_key = True)
    token = models.CharField(max_length = 32)

class UserAddress(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    address = models.CharField(max_length = 100)

    def __string__(self):
        return self.user + ' , ' + self.address
    
    def __unicode__(self):
        return self.user + ' , ' + self.address
