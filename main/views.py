# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import re

from .models import *
import blockchain.settings as settings
from . import mailer
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from . import blockchain

regex_string = r'^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.)?(iitk\.ac\.in)$'
reg_obj = re.compile(regex_string)
# Create your views here.

def signup(request):
    return render(request, 'main/signup.html',{})

def sendMail(request):
    token = uuid.uuid1().hex
    email = request.GET['email']
    if not reg_obj.match(email):
        return HttpResponse('Only iitk email allowed')
    qSet = EmailToken.objects.filter(email = email)
    if qSet.exists():
        obj = qSet[0]
        obj.token = token
        obj.save()
    else:
        EmailToken.objects.create(email = email, token = token)
    subject = 'Activation Token'
    body = "http://localhost:8000/main/createaccount/?email=%s&token=%s" %(email,token)
    mailer.send_mail_async(
            subject,
            body,
            email)
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
                    user = User(username = email, email = email, password = password1)
                    user.set_password(password1)
                    user.save()
                    return HttpResponse('User Created!')
                except:
                    user = User.objects.get(username = email)
                    user.set_password(password1)
                    user.save()
                    return HttpResponse('User Exists! Password Changed.')
        except:
            return HttpResponse('Email Does not exist!')

def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/main/index/')
    return render(request, 'main/signin.html', {})

@login_required
def index(request):
    return HttpResponse('Main Page')

@login_required
def addAddress(request):
    if request.method == 'POST':
        address = request.POST['address']
        user = request.user
        qSet = UserAddress.objects.filter(user = user)
        if qSet.exists():
            return HttpResponse('Address already associated!')
        UserAddress.objects.create(user = user, address = address)
        blockchain.add_voter_async(address)
        return HttpResponseRedirect('/main/index')
    return render(request,'main/addaddress.html', {})

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/main/login/')
