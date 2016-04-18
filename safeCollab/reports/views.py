from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from reports.models import Folder, Report, File
from django.core.context_processors import csrf
from reports.forms import UploadFileForm, DeleteFileForm
from django.utils.timezone import now

# Create your views here.

@login_required
def home(request):
	try:
		homeFolder = Folder.objects.filter(owner=request.user).filter(parentFolder=None)[0]
	except IndexError as e:
		homeFolder = Folder(owner=request.user, title="Home")
		homeFolder.save()
	folders = Folder.objects.filter(owner=request.user, parentFolder=homeFolder)
	reports = Report.objects.filter(collaborators=request.user, parentFolder=homeFolder)
	path = [homeFolder]
	c = Context({'folders': folders, 'reports': reports, 'path': path})
	c = RequestContext(request, c)
	return render(request, 'report_folder.html', c)

@login_required
def getReport(request, reportID):
	formset = {}
	if request.method == "POST":
		formset['uploadFileForm'] = UploadFileForm(request.POST, request.FILES)
		if formset['uploadFileForm'].is_valid():
			if(formset['uploadFileForm'].data['uploadDelete'] == 'upload'):
				newFile = File(content=request.FILES['file'], title=formset['uploadFileForm'].data['title'],
					publisher=request.user, timeStamp=now())
				newFile.save()
				instance = Report.objects.get(id=reportID)
				instance.files.add(newFile)
				instance.save()
		formset['deleteFileForm'] = DeleteFileForm(request.POST)
		if formset['deleteFileForm'].is_valid():
			if(formset['deleteFileForm'].data['uploadDelete'] == 'delete'):
				checkedFiles = request.POST.getlist('checkedFiles')
				for fileObj in checkedFiles:
					File.objects.get(id=fileObj).delete()
	else:
		formset = {'uploadFileForm': UploadFileForm(), 'deleteFileForm': DeleteFileForm()}
	report = Report.objects.get(id=reportID)
	path = [report]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'report': report, 'path': path, 'formset' : formset})
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

