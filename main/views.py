# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *
import blockchain.settings as settings

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.core import mail


import uuid

# Create your views here.

def signup(request):
    return render(request, 'main/signup.html',{})

def sendMail(request):
    token = uuid.uuid1().hex
    email = request.GET['email']
    qSet = EmailToken.objects.filter(email = email)
    if qSet.exists():
        obj = qSet[0]
        obj.token = token
        obj.save()
    else:
        EmailToken.objects.create(email = email, token = token)
    subject = 'Activation Token'
    body = "localhost:8000/main/createaccount/?email=%s&token=%s" %(email,token)
    mail.send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            ['jayaa@iitk.ac.in'],
            fail_silently=False,)
    return HttpResponseRedirect('/main/signup/')

def createAccount(request):
    if request.method == 'GET':
        email = request.GET['email']
        token = request.GET['token']
        context = {
                'email' : email,
                'token' : token
                }
        return render(request, 'main/createaccount.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        token = request.POST['token']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return HttpResponseRedirect('/main/createaccount/?email=%s&token=%s' %(email,token))
        try:
            dbObj = EmailToken.objects.get(email = email)
            if dbObj.token != token:
                return HttpResponse('Invalid Token!')
            else:
                try:
                    user = User.objects.create(username = email, email = email, password = password1)
                    return HttpResponse('User Created!')
                except:
                    return HttpResponse('User Exists!')
        except:
            return HttpResponse('Email Does not exist!')
