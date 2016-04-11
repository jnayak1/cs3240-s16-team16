from django import forms

class SendMessage(forms.Form):
	content = forms.CharField(widget=forms.Textarea)