from django.shortcuts import render
from django.template import Context
from django.contrib.auth.models import User
from private_messages.models import Message, ConversationLog
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

@login_required
def index(request):
	
	message_log = [("Me", "Hey Rodger!"), ("Rodger", "Hey! How's it going??"), ("Me", "Pretty good, hbu?")]
	contact_list = [["Rodger Nayak"], ["Katrin Nayak"], ["Kathrin Swoboda","Pradeep Nayak"]]
	c = Context({'conversation': message_log, 'contacts': contact_list})
	return render(request, 'private_messages.html', c)

