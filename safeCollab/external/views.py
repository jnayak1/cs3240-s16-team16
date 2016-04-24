from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from login.models import UserProfile
from reports.models import Report
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

    retVal = list()

    for profile in UserProfile.objects.all():
        user = profile.user
        name = user.username
        if username == name:
            groups = profile.groups.all()
            # retVal.append(name)
            # for x in groups:
            #     retVal.append(x.name)

    # retVal.append(str(Report.objects.filter(Q(group__in=groups)|Q(private=False)).all()))
    for report in Report.objects.filter(Q(group__in=groups.all())|Q(private=False)).all():
        retVal.append(report.title)

    return HttpResponse(json.dumps(retVal))