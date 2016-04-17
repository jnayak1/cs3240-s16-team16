from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from reports.models import Folder, Report, HomeFolder


# Create your views here.

@login_required
def home(request):
	folders = Folder.objects.filter(owner=request.user).exclude(parentFolder=None)
	reports = Report.objects.filter(collaborators=request.user)
	pwd = HomeFolder.objects.filter(owner=request.user)[0]
	c = Context({'folders': folders, 'reports': reports, 'pwd': pwd})
	c = RequestContext(request, c)
	return render(request, 'report_folder.html', c)

@login_required
def getReport(request, reportID):
	report = Report.objects.get(id=reportID)
	c = Context({'report': report})
	c = RequestContext(request, c)
	return render(request, 'report.html', c)

@login_required
def getFolder(request, folderID):
	folder = Folder.objects.filter(id=folderID)
	folders = Folder.objects.filter(owner=request.user, parentFolder=folder)
	reports = Report.objects.filter(collaborators=request.user, parentFolder=folder)
	pwd = Folder.objects.filter(owner=request.user)
	c = Context({'folders': folders, 'reports': reports, 'pwd': pwd})
	c = RequestContext(request, c)
	return render(request, 'report_folder.html', c)

