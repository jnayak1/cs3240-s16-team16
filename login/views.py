from django.template import RequestContext
from django.shortcuts import render_to_response
from login.models import Category
from django.shortcuts import render
from login.models import Page
from login.forms import CategoryForm
from login.forms import PageForm, UserForm, UserProfileForm, GroupingsForm, MyGroupingsForm, SiteManagerForm, DeleteUserForm, ActivateUserForm, DeactivateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import json
import string
import random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
from Crypto import Random

def index(request):
    # Request the context of the request.
    group_list = request.user.groups.all()
    context_dict = {'groups': group_list}

    # Render the response and send it back!
    return render(request, 'login/index.html', context_dict)
@login_required
def sample_add_member(request, group_id):
    group=Group.objects.get(pk=group_id)
    context_dict = {'groups': group}
    #return HttpResponse(group.name)
    return render(request, 'login/group.html', context_dict)

@login_required
def manage(request):
    users = User.objects.all()
    context_dict = {'users': users}
    return render(request, 'login/manage.html', context_dict)

@login_required
def deleteUser(request):
    done = False
    if request.method == 'POST':
        deleteForm = DeleteUserForm(data=request.POST)
        if(deleteForm.is_valid()):
            deleteuser = deleteForm.save()
            deleteuser.save()
            users = deleteForm.cleaned_data['username']
            for usr in users:
                usr.delete()
            done = True
        else:
            print(deleteForm.errors)
    else:
        deleteForm = DeleteUserForm()
    return render(request, 'login/delete_users.html', {'delete_form': deleteForm, 'done': done})

@login_required
def activate(request):
    done = False
    if request.method == 'POST':
        activateForm = ActivateUserForm(data=request.POST)
        if(activateForm.is_valid()):
            activateuser = activateForm.save()
            activateuser.save()
            users = activateForm.cleaned_data['username']
            for usr in users:
                usr.is_active = True
                usr.save()
            done = True
        else:
            print(activateForm.errors)
    else:
        activateForm = ActivateUserForm()
    return render(request, 'login/activate.html', {'activate_form': activateForm, 'done':done})

@login_required
def deactivate(request):
    done = False
    if request.method == 'POST':
        deactivateForm = DeactivateUserForm(data=request.POST)
        if(deactivateForm.is_valid()):
            deactivateuser = deactivateForm.save()
            deactivateuser.save()
            users = deactivateForm.cleaned_data['username']
            for usr in users:
                usr.is_active = False
                usr.save()
            done = True
        else:
            print(deactivateForm.errors)
    else:
        deactivateForm = DeactivateUserForm()
    return render(request, 'login/deactivate.html', {'deactivate_form': deactivateForm, 'done':done})



@login_required
def siteManager(request):
    done = False
    if request.method == 'POST':
        siteManager_form = SiteManagerForm(data = request.POST)
        if(siteManager_form.is_valid()):
            sitemanager = siteManager_form.save()
            sitemanager.save()
            staff = User.objects.filter(is_staff=True)
            staffNum = staff.count()
            if staffNum < 3:
                uname = siteManager_form.cleaned_data['name']
                user = User.objects.get(username=uname)
                user.is_staff = True
                user.save()
                groups = Group.objects.all()
                for grp in groups:
                    user.groups.add(grp)
                done = True
            else:
                done = False
                return HttpResponse("Cannot add site manager! More than three site managers already! <a href='/login/'>Return Home</a>")
        else:
            print (siteManager_form.errors)
    else:
        siteManager_form = SiteManagerForm()
    return render(request,
            'login/add_staffManager.html',
            {'staff_form': siteManager_form, 'done': done} )




@login_required
def mygroups(request):
# Sending user object to the form, to verify which fields to display/remove (depending on group)
    done = False
    if request.method == 'POST':
        mygroupings_form = MyGroupingsForm(data=request.POST) ####NEW!
# FIXME: edit the save database code stuffs. it doesn't actually add anyone to the groups.
# find oput how to display what groups you are in, not all the groups.
        # If the two forms are valid...
        if mygroupings_form.is_valid():# and group_form.is_valid():
            try:
                mygroupings = mygroupings_form.save()
                mygroupings.save()
                gobject = Group()
                gobject.name = mygroupings.name
                gobject.save()
               #groupings.members = members
            except IntegrityError as ex:
                return HttpResponse("Return back to previous page! <a href='/login/groups'></a>")

            request.user.groups.add(gobject)
#            for usr in groupings.members:
#            print (groupings.members)
            mems = mygroupings_form.cleaned_data['members']

# permission to identify group

# need to see what groups I am in, and be able to add others to any of those groups.

            staff = User.objects.filter(is_staff=True)
            for stf in staff:
                stf.groups.add(gobject)
            #gobject.user_set.add(the user)
            for usr in mems:
                usr.groups.add(gobject)

           # print (user.groups.all())
           # print (user.get_group_permissions(obj=None))
           # print (user.groups.filter(name='Reporter').exists())
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            done = True

        else:
            print (mygroupings_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        mygroupings_form = MyGroupingsForm()

    # Render the template depending on the context.
    return render(request,
            'login/mygroups.html',
            {'mygroupings_form': mygroupings_form, 'done': done} )


@login_required
def groups(request):
    done = False
    if request.method == 'POST':
        groupings_form = GroupingsForm(data=request.POST) ####NEW!

        # If the two forms are valid...
        if groupings_form.is_valid():# and group_form.is_valid():
            try:
                groupings = groupings_form.save()
                groupings.save()
                gobject = Group()
                gobject.name = groupings.name
                gobject.save()
               #groupings.members = members
            except IntegrityError as ex:
                return HttpResponse("Return to previous page, there was a problem <a href='/login/groups'></a>")

            request.user.groups.add(gobject)
#            for usr in groupings.members:
#            print (groupings.members)
            mems = groupings_form.cleaned_data['members']

# permission to identify group

# need to see what groups I am in, and be able to add others to any of those groups.


            #gobject.user_set.add(the user)

            staff = User.objects.filter(is_staff=True)
            for stf in staff:
                stf.groups.add(gobject)

                
            for usr in mems:
                usr.groups.add(gobject)

           # print (user.groups.all())
           # print (user.get_group_permissions(obj=None))
           # print (user.groups.filter(name='Reporter').exists())
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            done = True

        else:
            print (groupings_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        groupings_form = GroupingsForm()

    # Render the template depending on the context.
    return render(request,
            'login/groups.html',
            {'groupings_form': groupings_form, 'done': done} )


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/login/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login/login_page.html', {})



def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    private_key = ""

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            random_generator = Random.new().read
            key = RSA.generate(1024, random_generator)
            private_key = key.exportKey()
            # print(key.publickey().exportKey())
            # print(len(key.publickey().exportKey()))
            profile = profile_form.save(commit=False)
            profile.public_key = key.publickey().exportKey()
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
        'login/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'private_key': private_key} )

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'login/add_page.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'login/add_category.html', {'form': form})

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'login/category.html', context_dict)