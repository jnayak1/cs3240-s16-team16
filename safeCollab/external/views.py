from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from login.models import UserProfile
from reports.models import Report, File
from django.db.models import Q

import json
import string
import random

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
from Crypto import Random

from .models import Tracker
import binascii
import os

#Create your views here.
# def login(request):
#     return HttpResponse(json.dumps("The query was successful!"))

@csrf_exempt
def login(request, username, password):
    #will be the random string to authenticate with in the standalone application
    retVal = ''

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
        # Is the account active? It could have been disabled.
        if user.is_active:
            retVal = retVal.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(256))
            invalid_sessions = Tracker.objects.filter(username = username)
            for tracker in invalid_sessions:
                tracker.delete()
            signedInUser = Tracker()
            signedInUser.key = retVal
            signedInUser.username = username
            signedInUser.save()
            return HttpResponse(json.dumps(retVal))
        else:
            # An inactive account was used - no logging in!
            return HttpResponse(json.dumps("Your safeCollab account is disabled."))
    else:
        # Bad login details were provided. So we can't log the user in.
        return HttpResponse(json.dumps("Invalid login details supplied."))

@csrf_exempt
def logout(request, userkey):
    #Delete the user's ad hoc "session" if it exists
    user_entry = Tracker.objects.filter(key=userkey)
    user_entry.delete()
    return HttpResponse(json.dumps("If you were logged in through the stand-alone application, your session was destroyed."))

@csrf_exempt
def getReports(request, username, userkey):

    retVal = {}
    groups = Group.objects.none()

    for profile in UserProfile.objects.all():
        user = profile.user
        name = user.username
        if username == name:
            groups = profile.groups.all()

    counter = 0
    for report in Report.objects.filter(Q(group__in=groups.all())|Q(private=False)).all():
        retVal["report" + str(counter)] = report.title
        counter+=1

    return HttpResponse(json.dumps(retVal), content_type="application/json")

@csrf_exempt
def verifyUser(request, username, userkey):

    # Verify that there is an active offline session
    session = Tracker.objects.filter(username = username, key = userkey)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if session:
        return HttpResponse(json.dumps("You have an active session."))
    else:
        # Bad login details were provided. So we can't log the user in.
        return HttpResponse(json.dumps("You do not have an active session."))

@csrf_exempt
def receiveFile(request, username, userkey, file_name, encrypted):
    uploaded_file = request.FILES[file_name]
    file = File()
    if encrypted == "True":
        file.title = file_name + '.enc'
        file.encrypted = True
    else:
        file.title = file_name
        file.encrypted = False
    file.content = uploaded_file.read()
    # with reopen_binary(uploaded_file) as binaryInformation:
    #     file.content = binaryInformation.read()
    user = User.objects.get(username=username)
    if not user==None:
        file.publisher = user
        file.save()
        return HttpResponse(json.dumps("File upload successful."))
    else:
        HttpResponse(json.dumps("File upload failed."))

@csrf_exempt
def seeReport(request, username, report_name):
    report = Report.objects.get(title = report_name)
    if not report == None:
        retVal = {}
        retVal['Title'] = report.title
        retVal['Short'] = report.shortDescription
        retVal['Long'] = report.longDescription
        counter = 0
        files = list()
        for file in report.files.all():
            files.append(file.title)
            counter+=1
        retVal['Files'] = files
        retVal['Owner'] = report.owner.username
        return HttpResponse(json.dumps(retVal))
    else:
        return HttpResponse(json.dumps("Failed to get report info"))

@csrf_exempt
def getFile(request, username, file_name):
    file = File.objects.get(title = file_name)
    if not file == None:
        content = file.content
        return HttpResponse(content)
        # response = HttpResponse(FileWrapper(retVal), content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename=' + file_name
    else:
        return HttpResponse("Failed to retrieve file")