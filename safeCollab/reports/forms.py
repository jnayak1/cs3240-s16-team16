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