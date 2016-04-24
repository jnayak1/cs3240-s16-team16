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
from reports.forms import UploadFileForm, DeleteFileForm, AddCollaboratorForm, DeleteCollaboratorForm, EditSummaryForm, EditDescriptionForm, AddFolderForm, AddReportForm, RemoveReportFolderForm
from django.utils.timezone import now
from itertools import chain

# Create your views here.

@login_required
def home(request):
	if not request.user.is_authenticated():
		return HttpResponse(request.user.is_authenticated())
	# redirect to get folder
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
	return HttpResponseRedirect('/reports/folder/' + str(homeFolder.id))

@login_required
def getReport(request, reportID):
	if not request.user.is_authenticated():
		return HttpResponse("You are not authorized to access that location.")
	formset = {}
	report = Report.objects.get(id=reportID)
	if request.method == "POST":
		formset['editSummaryForm'] = EditSummaryForm(request.POST)
		if formset['editSummaryForm'].is_valid():
			report.shortDescription = formset['editSummaryForm'].data['summary']
			report.save()
		formset['editDescriptionForm'] = EditDescriptionForm(request.POST)
		if formset['editDescriptionForm'].is_valid():
			report.longDescription = formset['editDescriptionForm'].data['description']
			report.save()
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
		formset['addCollaboratorForm'] = AddCollaboratorForm(request.POST)
		if formset['addCollaboratorForm'].is_valid():
			if(formset['addCollaboratorForm'].data['addDelete'] == 'add'):
				addedUser = User.objects.get(email=formset['addCollaboratorForm'].data['email'])
				report.collaborators.add(addedUser)
				report.save()
		formset['deleteCollaboratorForm'] = DeleteCollaboratorForm(request.POST)
		if formset['deleteCollaboratorForm'].is_valid():
			if(formset['deleteCollaboratorForm'].data['addDelete'] == 'delete'):
				for collabObj in request.POST.getlist('checkedCollaborators'):
					deletedCollaborator = User.objects.get(id=collabObj) 
					report.collaborators.remove(deletedCollaborator)
	else:
		formset = {
			'editDescriptionForm' : EditDescriptionForm(),
			'editSummaryForm' : EditSummaryForm(),
			'uploadFileForm': UploadFileForm(), 
			'deleteFileForm': DeleteFileForm(),
			'addCollaboratorForm' : AddCollaboratorForm(), 
			'deleteCollaboratorForm' : DeleteCollaboratorForm()}
	path = [report]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'report': report, 'path': path, 'formset' : formset})
	c = RequestContext(request, c)
	return render(request, 'report.html', c)

@login_required
def getFolder(request, folderID):
	if not request.user.is_authenticated():
		return HttpResponse("You are not authorized to access that location.")
	formset = {}
	pwd = Folder.objects.get(id=folderID)
	if request.method == "POST":
		formset['addFolderForm'] = AddFolderForm(request.POST)
		if formset['addFolderForm'].is_valid():
			if formset['addFolderForm'].data['reportFolder'] == 'folder':
				newFolder = Folder(owner=request.user, title=formset['addFolderForm'].data['name'],parentFolder=pwd)
				newFolder.save()
		formset['addReportForm'] = AddReportForm(request.POST)
		print(formset['addReportForm'].errors)
		if formset['addReportForm'].is_valid():
			if formset['addReportForm'].data['reportFolder'] == 'report':
				print("hello")
				newReport = Report.objects.create(owner=request.user, title=formset['addReportForm'].data['title'],
					parentFolder=pwd)
				newReport.save()
	else:
		formset = {
			'addFolderForm': AddFolderForm(),
			'addReportForm': AddReportForm(),
			'removeReportFolderForm': RemoveReportFolderForm()
		}
	folders = Folder.objects.filter(owner=request.user, parentFolder=pwd)
	reports = Report.objects.filter(collaborators=request.user, parentFolder=pwd)
	reports = list(chain(reports, Report.objects.filter(owner=request.user, parentFolder=pwd)))
	path = [pwd]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'folders': folders, 'reports': reports, 'path': path, 'pwd':pwd})
	c = RequestContext(request, c)
	c['formset'] = formset
	return render(request, 'report_folder.html', c)

