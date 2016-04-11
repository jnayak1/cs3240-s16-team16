from django import forms

class SendMessage(forms.Form):
	content = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super(SendMessage, self).__init__(*args, **kwargs)
		self.fields['content'].widget.attrs['rows'] = 5
		self.fields['content'].widget.attrs['cols'] = 90