from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from private_messages.models import Message, ConversationLog
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from private_messages.forms import SendMessage
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def index(request):
	conversations = ConversationLog.objects.all()
	c = Context({'conversations': conversations})
	if request.method == 'POST':
		form = SendMessage(request.POST)
		if form.is_valid():
			send_message = SendMessage(request.POST)
			message_content = send_message.data['content']
			message_sender = request.user
			message = Message(sender=message_sender, content=message_content)
			message.save()
	else:
		form = SendMessage()
	c['form'] = form
	c = RequestContext(request, c)
	return render(request, 'private_messages.html', c)

def getConversation(request, conversationID):
	conversations = ConversationLog.objects.all()
	active_conversation = ConversationLog.objects.get(pk=conversationID)
	c = Context({'conversations': conversations, 'active_conversation': active_conversation})
	if request.method == 'POST':
		form = SendMessage(request.POST)
		if form.is_valid():
			send_message = SendMessage(request.POST)
			message_content = send_message.data['content']
			message_sender = request.user
			message = Message(sender=message_sender, content=message_content)
			message.save()
			active_conversation.log.add(message)
	else:
		form = SendMessage()
	c['form'] = form
	c = RequestContext(request, c)
	return render(request, 'private_messages.html', c)

