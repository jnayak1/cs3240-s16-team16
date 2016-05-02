from django import forms
from .models import SignUp, PublicKey

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']

    def clean_email(self):
        #print will print to the command prompt
        email = self.cleaned_data.get("email")
        email_base, provider = email.split("@")
        domain, extension = provider.split(".")
        if not domain == "virginia":
            raise forms.ValidationError("Please use your UVa email")
        if not extension == "edu":
            raise forms.ValidationError("Please use a valid .edu email address")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        return full_name

class PublicKeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['file', 'key']

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length = 50)
    file = forms.FileField()