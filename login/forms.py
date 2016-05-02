from django import forms
from login.models import Page, Category, UserProfile, Groupings, SiteManager, ActivateUser, DeactivateUser, DeleteUser
from django.contrib.auth.models import User, Group

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class SiteManagerForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, help_text="Please choose a user.")
    class Meta:
        model = SiteManager
        fields = ('name',)

class GroupingsForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Groupings
        fields = ('name', 'members')

class MyGroupingsForm(forms.ModelForm):
    mygroups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Groupings
        fields = ('members', 'mygroups')

class ActivateUserForm(forms.ModelForm):
    username = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=False), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = ActivateUser
        fields = {'username',}

class DeactivateUserForm(forms.ModelForm):
    username = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = DeactivateUser
        fields = {'username',}

class DeleteUserForm(forms.ModelForm):
    username = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = DeleteUser
        fields = {'username',}
   



class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)