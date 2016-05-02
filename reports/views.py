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
from reports.forms import RemoveReportFolderForm, UploadFileForm, DeleteFileForm, AddCollaboratorForm, DeleteCollaboratorForm, EditSummaryForm, EditDescriptionForm, AddFolderForm, AddReportForm, MoveForm, SearchForm, EditKeyWords
from django.utils.timezone import now
from itertools import chain
from login.models import UserProfile
from django.db.models import Q
import re
from django.contrib import messages

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
	if not Report.objects.filter(id=reportID).exists():
		messages.error(request, 'Report does not exist.')
		return HttpResponseRedirect('/reports/')

	# report exists so there shouldn't be any exceptions
	report = Report.objects.get(id=reportID)

	formset = {}
	reportGroup = report.group

	# if user is not in the group for the report and report is private, direct to home folder
	if (not(request.user.groups.filter(id=reportGroup.id).exists()) and report.private == True):
		messages.error(request,"You do not have access to the requested report.")
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
		formset['editKeyWords'] = EditKeyWords(request.POST)
		if formset['editKeyWords'].is_valid():
			report.keywords = formset['editKeyWords'].data['keywords']
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
				try:
					addedUser = User.objects.get(email=formset['addCollaboratorForm'].data['email'])
					addedUser.groups.add(reportGroup)
				except User.DoesNotExist:
					messages.error(request, "The user does not exist.")
					return HttpResponseRedirect('/reports/' + str(reportID))
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
			'editKeyWords' : EditKeyWords(),
			'uploadFileForm': UploadFileForm(), 
			'deleteFileForm': DeleteFileForm(),
			'addCollaboratorForm' : AddCollaboratorForm(), 
			'deleteCollaboratorForm' : DeleteCollaboratorForm()}
	# This gives that path. It currently is not working since we changed models.py.
	path = []
	try:
		path = [Folder.objects.get(reports__id=report.id, owner=request.user)]
		while path[0].parentFolder != None:
			path.insert(0,path[0].parentFolder)
	except Folder.DoesNotExist as e:
		pass
	collaboratingUsers = reportGroup.user_set.all()
	owner = request.user == report.owner
	private = report.private
	c = Context({'report': report, 'path': path, 'formset' : formset, 
		"collaboratingUsers": collaboratingUsers, 'owner': owner, 'private': private})
	c = RequestContext(request, c)
	return render(request, 'report.html', c)

@login_required
def togglePrivate(request, reportID):
	report = Report.objects.get(id=reportID)
	if request.user == report.owner:
		report.private = not report.private
		report.save()
	else:
		messages.error(request, "You are not the owner of the report so you cannot change privacy.")
	return HttpResponseRedirect('/reports/' + reportID)

@login_required
def deleteReport(request, reportID):
	report = Report.objects.get(id=reportID)
	parentFolder = Folder.objects.get(reports__id=reportID)
	if request.user == report.owner:
		report.delete()
	else:
		messages.error("You are not the owner of the report so you cannot delete the")
	return HttpResponseRedirect('/reports/folder/' + str(parentFolder.id))

@login_required
def getFolder(request, folderID):
	# redirect to home folder if folder does not exist
	if not Folder.objects.filter(id=folderID).exists():
		messages.error(request, "Requested folder does not exist.")
		return HttpResponseRedirect('/reports/')
	formset = {}
	pwd = Folder.objects.get(id=folderID)

	# if user does not own folder, redirect to home folder
	if (pwd.owner != request.user):
		messages.error(request, "You do not have access to the requested folder.")
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
				# group must exist 
				if not Group.objects.filter(name=formset['addReportForm'].data['reportGroup']).exists():
					messages.error("Group does not exist.")
					return HttpResponseRedirect('/reports/folder/' + str(folderID))

				collaboratingGroup = Group.objects.get(name=formset['addReportForm'].data['reportGroup'])

				# owner must be a part of group
				if not request.user.groups.filter(name=collaboratingGroup.name).exists():
					messages.error(request, "You cannot create a report with a group you are not a part of.")
					return HttpResponseRedirect('/reports/folder/' + str(folderID))

				# report title must be unique
				if Report.objects.filter(title=formset['addReportForm'].data['title']):
					messages.error(request, "There is already a report named" + formset['addReportForm'].data['title'])
					return HttpResponseRedirect('/reports/folder/' + str(folderID))
				print("adding report")
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

		formset['searchForm'] = SearchForm(request.POST)
		if formset['searchForm'].is_valid():
			report.search = formset['searchForm'].data['search']
			report.save()
		formset['moveForm'] = MoveForm(request.POST)
		if formset['moveForm'].is_valid():
			folderID = request.POST.get('selectedFolders')
			try:
				destinationFolder = Folder.objects.get(id=folderID)
			except Exception as e:
				#return render(request, 'report_folder.html', c)
				print("Exception!")
			for item in request.POST.getlist('selectedFolders'):
				folderToMove = Folder.objects.get(id=item)
				folderToMove.parentFolder = destinationFolder
				folderToMove.save()
			for item in request.POST.getlist('selectedReports'):
				reportToMove = Report.objects.get(id=item)
				try:
					destinationFolder.reports.add(reportToMove)
					destinationFolder.save()
				except Exception as e:
					print("Exception! Adding to destination folder!")

				
			if request.POST.get('moveButton') == "Move":
				try:
					destinationFolderID = request.POST.get('destinationFolder')
					destinationFolder = Folder.objects.get(id=destinationFolderID)

					for item in request.POST.getlist('selectedFolders'):
						folderToMove = Folder.objects.get(id=item)
						folderToMove.parentFolder = destinationFolder
						folderToMove.save()
					for item in request.POST.getlist('selectedReports'):
						reportToMove = Report.objects.get(id=item)
						destinationFolder.reports.add(reportToMove)
						destinationFolder.save()
					for item in request.POST.getlist('selectedReports'):
						pwd.reports.remove(Report.objects.get(id=item))
				except Exception:
					messages.error(request, "Invalid move operation.")
					HttpResponseRedirect('/reports/folder' + str(folderID))
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

@login_required
def search(request, searchID):
	reportWithSearchTitle = []
	reportWithSearchTitle.append("WEE!")
	allreports = Report.objects.all()
	if request.method == 'POST':
		#searchForm = SearchForm(request.POST)

		allreports = Report.objects.all()
		search_terms = request.POST['searchKey']
		pattern = re.compile("\\s+")
		keywords = pattern.split(search_terms)
		
		for keyword in keywords:
			if keyword in allreports.values_list('title', flat=True):
				reportWithSearchTitle.append(keyword)
				return render(request, 'report_search.html', {})
				

		#return HttpResponse(keywords[1])
	return render(request, 'report_search.html', {})

def search(request):
	if request.method == 'POST':
		reportWithSearchTitle = []
		reportWithMatchingTags = []
		reportWithMatchingSummary = []
		reportWithMatchingDescription = []

		groups = request.user.groups.all()

		allreports = Report.objects.filter(Q(group__in=groups.all())|Q(private=False)).all()
	    #allreports = Report.objects.filter(Q(group__in=groups.all())|Q(private=False)).all()
		appeared = []
		reports = Report.objects.all()
		#allreports = Report.objects.filter(user=request.user)
		search_terms = request.POST['searchKey']
		pattern = re.compile("\\s+")
		keywords = pattern.split(search_terms)
		
		for keyword in keywords:
			boolean = False
			if keyword in allreports.values_list('title', flat=True):
				report = Report.objects.get(title=keyword)
				reportWithSearchTitle.append(report)
				appeared.append(keyword)
				boolean = True
			
			for report in allreports:
				title = Report.objects.get(title=report.title)
				tags = pattern.split(report.keywords)
				for tag in tags:
					if (keyword == tag) and (keyword not in appeared) and not boolean:
						reportWithMatchingTags.append(title)
						appeared.append(keyword)
						boolean = True
						break
				summary = pattern.split(report.shortDescription)
				for summ in summary:
					if (keyword == summ) and (keyword not in appeared) and not boolean:
						reportWithMatchingSummary.append(title)
						appeared.append(keyword)
						boolean = True
						break
						#return HttpResponse(keyword)
				descriptions = pattern.split(report.longDescription)
				for description in descriptions:
					if (keyword == description) and (keyword not in appeared) and not boolean:
						reportWithMatchingDescription.append(title)
						appeared.append(keyword)
						boolean = True
						break
	context = {
		'reportWithSearchTitle' : reportWithSearchTitle,
		'reportWithMatchingTags' : reportWithMatchingTags,
		'reportWithMatchingSummary' : reportWithMatchingSummary,
		'reportWithMatchingDescription' : reportWithMatchingDescription
		}				
	return render(request, 'report_search.html', context)	

