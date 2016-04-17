from django import forms
from private_messages.models import ConversationLog

class AddFile(forms.Form):
	name = forms.CharField(max_length=100)

class RemoveFile(forms.Form):
	pass
