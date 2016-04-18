from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from reports.models import Folder, Report


# Create your views here.

@login_required
def home(request):
	#Please fix. 
	array = Folder.objects.filter(owner=request.user).filter(parentFolder=None)
	
	if len(array) > 0:
		homeFolder = Folder.objects.filter(owner=request.user).filter(parentFolder=None)[0]
		folders = Folder.objects.filter(owner=request.user).exclude(parentFolder=None)
		reports = Report.objects.filter(collaborators=request.user, parentFolder=homeFolder)
		path = [homeFolder]
		c = Context({'folders': folders, 'reports': reports, 'path': path})
		c = RequestContext(request, c)
		return render(request, 'report_folder.html', c)
	else:
		return HttpResponse("There are no folders.")

@login_required
def getReport(request, reportID):
	report = Report.objects.get(id=reportID)
	path = [report]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'report': report, 'path': path})
	c = RequestContext(request, c)
	return render(request, 'report.html', c)

@login_required
def getFolder(request, folderID):
	pwd = Folder.objects.get(id=folderID)
	folders = Folder.objects.filter(owner=request.user, parentFolder=pwd)
	reports = Report.objects.filter(collaborators=request.user, parentFolder=pwd)
	path = [pwd]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'folders': folders, 'reports': reports, 'path': path, 'pwd':pwd})
	c = RequestContext(request, c)
	return render(request, 'report_folder.html', c)

