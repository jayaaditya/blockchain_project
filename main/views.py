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

userAddress = {}

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
    return HttpResponse('Email sent to %s. Click <a href="/main/sendmail/?email=%s">here</a> to resend.'%(email,email))

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
                    return HttpResponseRedirect('/main/login/')
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

@user_passes_test(lambda u: u.is_superuser)
def index2(request):
    if request.method == 'POST':
        name = request.POST['name']
        name.strip()
        if name != '':
            blockchain.add_candidate_async(name)
        return HttpResponseRedirect('/main/index2')
    return render(request, 'main/index2.html', {})

@user_passes_test(lambda u: u.is_superuser)
def stopPolling(request):
    blockchain.stop_polling_async()
    return HttpResponseRedirect('/main/index2/')

@login_required
def index(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/main/index2/')
    return render(request, 'main/index.html')

@login_required
def addAddress(request):
    if request.method == 'POST':
        address = request.POST['address']
        user = request.user.username
        if user in userAddress:
            return HttpResponse('Address already associated!')
        blockchain.add_voter_async(address)
        userAddress[user] = address
        return HttpResponseRedirect('/main/index')
    if request.user.username in userAddress:
        return HttpResponseRedirect('/main/index')
    return render(request,'main/addaddress.html', {})

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/main/login/')
