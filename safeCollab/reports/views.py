from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from reports.models import Folder, Report, File
from django.core.context_processors import csrf
from reports.forms import RemoveReportFolderForm, UploadFileForm, DeleteFileForm, AddCollaboratorForm, DeleteCollaboratorForm, EditSummaryForm, EditDescriptionForm, AddFolderForm, AddReportForm, MoveForm 
from django.utils.timezone import now
from itertools import chain

# Create your views here.

@login_required
def home(request):
	# redirect to get folder
	try:
		homeFolder = Folder.objects.filter(owner=request.user).filter(parentFolder=None)[0]
	except IndexError as e:
		homeFolder = Folder(owner=request.user, title="Home")
		homeFolder.save()
	return HttpResponseRedirect('/reports/folder/' + str(homeFolder.id))

@login_required
def getReport(request, reportID):
	formset = {}
	report = Report.objects.get(id=reportID)
	reportGroup = report.group

	# if user is not in the group for the report and report is private, direct to home folder
	if (not(request.user.groups.filter(id=reportGroup.id).exists()) && report.private == True):
		return HttpResponseRedirect('/reports/')

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
				addedUser.groups.add(reportGroup)
		formset['deleteCollaboratorForm'] = DeleteCollaboratorForm(request.POST)
		if formset['deleteCollaboratorForm'].is_valid():
			if(formset['deleteCollaboratorForm'].data['addDelete'] == 'delete'):
				for collabObj in request.POST.getlist('checkedCollaborators'):
					deletedCollaborator = User.objects.get(id=collabObj) 
					deletedCollaborator.groups.remove(reportGroup)
	else:
		formset = {
			'editDescriptionForm' : EditDescriptionForm(),
			'editSummaryForm' : EditSummaryForm(),
			'uploadFileForm': UploadFileForm(), 
			'deleteFileForm': DeleteFileForm(),
			'addCollaboratorForm' : AddCollaboratorForm(), 
			'deleteCollaboratorForm' : DeleteCollaboratorForm()}
	# This gives that path. It currently is not working since we changed models.py.
	path = [Folder.objects.filter(reports__id=report.id, owner=request.user)[0]]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	collaboratingUsers = reportGroup.user_set.all()
	c = Context({'report': report, 'path': path, 'formset' : formset, "collaboratingUsers": collaboratingUsers})
	c = RequestContext(request, c)
	return render(request, 'report.html', c)

@login_required
def getFolder(request, folderID):
	formset = {}
	pwd = Folder.objects.get(id=folderID)

	# if user does not own folder, redirect to home folder
	if (pwd.owner != request.user):
		return HttpResponseRedirect('/reports/')

	if request.method == "POST":
		formset['addFolderForm'] = AddFolderForm(request.POST)
		if formset['addFolderForm'].is_valid():
			if formset['addFolderForm'].data['reportFolder'] == 'folder':
				newFolder = Folder(owner=request.user, title=formset['addFolderForm'].data['name'],parentFolder=pwd)
				newFolder.save()
		
		formset['addReportForm'] = AddReportForm(request.POST)
		if formset['addReportForm'].is_valid():
			if formset['addReportForm'].data['reportFolder'] == 'report':
				collaboratingGroup = Group.objects.create(name=formset['addReportForm'].data['title'])
				collaboratingGroup.save()
				request.user.groups.add(collaboratingGroup)
				newReport = Report.objects.create(owner=request.user, title=formset['addReportForm'].data['title'],
					group=collaboratingGroup)
				newReport.save()
				pwd.reports.add(newReport)
				pwd.save()
		formset['removeReportFolderForm'] = RemoveReportFolderForm(request.POST)
		if formset['removeReportFolderForm'].is_valid():
			if request.POST.get('deleteButton') == "Delete":
				print("deleted")
				for fdr in request.POST.getlist('selectedFolders'):
					deletedFolder = Folder.objects.get(id=fdr)
					deletedFolder.delete()
				for rpt in request.POST.getlist('selectedReports'):
					deletedReport = Report.objects.get(id=rpt)
					pwd.reports.remove(deletedReport)

				
		formset['moveForm'] = MoveForm(request.POST)
		if formset['moveForm'].is_valid():
			if request.POST.get('moveButton') == "Move":
				destinationFolderID = request.POST.get('destinationFolder')
				destinationFolder = Folder.objects.get(id=destinationFolderID)
				print(request.POST.getlist('selectedReports'))
				for item in request.POST.getlist('selectedFolders'):
					folderToMove = Folder.objects.get(id=item)
					folderToMove.parentFolder = destinationFolder
					folderToMove.save()
				for item in request.POST.getlist('selectedReports'):
					reportToMove = Report.objects.get(id=item)
					destinationFolder.reports.add(reportToMove)
					destinationFolder.save()
					pwd.reports.remove(reportToMove)
					pwd.save()
	else:
		formset = {
			'addFolderForm': AddFolderForm(),
			'addReportForm': AddReportForm(),
			'removeReportFolderForm': RemoveReportFolderForm(),
			'moveForm':MoveForm()
		}

	folders = Folder.objects.filter(owner=request.user, parentFolder=pwd)
	reports = pwd.reports.all
	path = [pwd]
	while path[0].parentFolder != None:
		path.insert(0,path[0].parentFolder)
	path.pop()
	c = Context({'folders': folders, 'reports': reports, 'path': path, 'pwd': pwd})
	c = RequestContext(request, c)
	c['formset'] = formset
	return render(request, 'report_folder.html', c)

