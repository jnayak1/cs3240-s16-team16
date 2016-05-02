from django import forms
from private_messages.models import ConversationLog
class SendMessage(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
	encrypted = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		super(SendMessage, self).__init__(*args, **kwargs)
		self.fields['content'].widget.attrs['rows'] = 5
		self.fields['content'].widget.attrs['cols'] = 90

class ConversationForm(forms.Form):
	participants = forms.CharField(widget=forms.Textarea)
	log = forms.CharField(widget=forms.Textarea)
	#class Meta:
#		model = ConversationLog
#		fields = ('participants', 'log')
