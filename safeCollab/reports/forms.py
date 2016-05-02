from django import forms

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()
	CHOICES=[('upload','upload'),
		('delete','delete')]
	uploadDelete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class DeleteFileForm(forms.Form):
	CHOICES=[('upload','upload'),
		('delete','delete')]
	uploadDelete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class AddCollaboratorForm(forms.Form):
	CHOICES=[('add','delete'),
		('add','delete')]
	addDelete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	email = forms.EmailField()

class DeleteCollaboratorForm(forms.Form):
	CHOICES=[('add','delete'),
		('delete','delete')]
	addDelete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class EditSummaryForm(forms.Form):
	summary = forms.CharField(widget=forms.Textarea)

class EditDescriptionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea)

class EditKeyWords(forms.Form):
	keywords = forms.CharField(widget=forms.Textarea)

class SearchForm(forms.Form):
	search = forms.CharField(widget=forms.Textarea)

class AddFolderForm(forms.Form):
	CHOICES=[('report','report'),
		('folder','folder')]
	reportFolder = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	name = forms.CharField(max_length=50)

class AddReportForm(forms.Form):
	CHOICES=[('report','report'),
		('folder','folder')]
	reportFolder = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	title = forms.CharField(max_length=50)
	reportGroup = forms.CharField(max_length=50)

class RemoveReportFolderForm(forms.Form):
	pass

class MoveForm(forms.Form):
	pass
