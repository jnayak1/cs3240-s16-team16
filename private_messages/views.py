from django.shortcuts import render
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from private_messages.models import Message, ConversationLog
from login.models import UserProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from private_messages.forms import SendMessage, ConversationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import re
import binascii

import json
import string
import random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
from Crypto import Random


def encrypt(message_content, key):
	rsa_key = RSA.importKey(key)
	public_key = rsa_key.publickey()
	retVal = public_key.encrypt(message_content, 32)[0]
	print(retVal)
	return retVal

def decrypt(message_content, key):
	print("decrypt:" + str(message_content))
	rsa_key = RSA.importKey(key)
	decryptable = (message_content,)
	retVal = rsa_key.decrypt(decryptable)
	return retVal

@login_required
def unread_messages(request):
	num_unread = 0;
	users_conversations = []
	allconversations = ConversationLog.objects.all()
	for conversation in allconversations:
		if request.user in conversation.participants.all():
			users_conversations.append(conversation)
	for conversation in users_conversations:
		if not conversation.filter(readBy__id=request.user.id).exists():
			num_unread = num_unread + 1;
	return num_unread

@login_required
def index(request):
	allconversations = ConversationLog.objects.all()
	conversations = []
	for conversation in allconversations:
		if request.user in conversation.participants.all():
			conversations.append(conversation)
	c = Context({'conversations': conversations, 'user': request.user})
	c = RequestContext(request, c)
	return render(request, 'private_messages.html', c)

@login_required
def getConversation(request, conversationID):
	allconversations = ConversationLog.objects.all()
	conversations = []
	for conversation in allconversations:
		if request.user in conversation.participants.all():
			conversations.append(conversation)
	# if conversation does not exist, go back to /private_messages/
	if not ConversationLog.objects.filter(id=conversationID).exists():
		messages.error(request, "That conversation does not exist.")
		return HttpResponseRedirect("/private_messages/")

	active_conversation = ConversationLog.objects.get(pk=conversationID)
	active_conversation.readBy.add(request.user)

	decrypted_active_conversation = []

	for message in active_conversation.log.all():
		if message.encrypted and request.method == 'POST' and request.POST.get('keybutton') == "Submit":
		# try:
			print("decrypting")
			key = request.POST.get('privatekey')
			print(key)
			decrypted_message = decrypt(message.content, key)
			decrypted_active_conversation.append(decrypted_message)
			# except Exception:
			print("Decrypting of message threw exception")
			decrypted_active_conversation.append(message)
		else:
			decrypted_active_conversation.append(message)
	# if user is not in the conversation, redirect to /private_messages/
	if request.user not in active_conversation.participants.all():
		messages.error(request, "You are not in that conversation.")
		return HttpResponseRedirect('/private_messages/')
	c = Context({'conversations': conversations, 'decrypted_active_conversation': decrypted_active_conversation,
		'active_conversation': active_conversation})
	if request.method == 'POST':
		form = SendMessage(request.POST)
		if form.is_valid():
			send_message = SendMessage(request.POST)
			message_content = send_message.data['content'].encode()
			message_sender = request.user
			message_receiver = active_conversation.participants.all().exclude(id=request.user.id)
			isEncrypted = False;
			try:
				isEncrypted = send_message.data['encrypted']
			except Exception:
				pass
			if isEncrypted:
				# encrypted_message = encrypt(message_content)
				# message_content = encrypt(message_content)[0]
				publickey = UserProfile.objects.get(user=message_receiver).public_key
				message_content = encrypt(message_content, publickey)
				print(message_content)
			message = Message(sender=message_sender, content=message_content, encrypted=isEncrypted)
			message.save()
			active_conversation.log.add(message)
	else:
		form = SendMessage()
	c['form'] = form
	c = RequestContext(request, c)
	return render(request, 'private_messages.html', c)

@login_required
def newConversation(request):
	#if request.method == 'POST':
	#	form = 
	#active_conversation = ConversationLog.objects.get(pk=conversationID)
	#c = Context({'conversations': conversations, 'active_conversation':active_conversation})
	if request.method == 'POST':
		conversationForm = ConversationForm()
		#if conversationForm.is_valid():
		new_conversation = ConversationForm(request.POST)
		participants = new_conversation.data['participants']
		log = new_conversation.data['message']
		pattern = re.compile("^\s+|\s*,\s*|\s+$")
		if (participants != "") and (log != ""):
			users = []
			nonexistentusers = []
			for x in pattern.split(participants):
				if x:
					if x in User.objects.all().values_list('username', flat=True):
						users.append(x)
					else:
						nonexistentusers.append(x)
			if len(nonexistentusers) > 0:
				printout = "The following users do not exist: "
				for y in nonexistentusers:
					printout += y
					printout += " "
				printout += ". Please send the message again."
				return HttpResponse(printout)
			else:
				active_conversation = ConversationLog()
				active_conversation.save()
				#userobjects = []
				for x in users:
					active_conversation.participants.add(User.objects.get(username=x))
					#userobjects.append(User.objects.get(username=x))
					#p = "HELLO "
					#p+=str(currentUser)
					#return HttpResponse(p)
					#conversation.participants.add(currentUser)
				
				active_conversation.participants.add(User.objects.get(username=request.user))
				message_sender = request.user
				message = Message(sender=message_sender, content=bytes(log, "UTF-8"))
				message.save()
				active_conversation.log.add(message)
				active_conversation.save()
				return HttpResponseRedirect('/private_messages')
				
			#return HttpResponse(users[0])
			#return HttpResponse([x for x in users if x])
		else:
			return HttpResponse("One or more of your fields is blank.")
			#return HttpResponse("WOAH")	
		#return HttpResponse(participants)
		#return HttpResponse("WOAH")
	else:
		conversationForm = ConversationForm()
		
		
	return render(request, 'new_conversation.html', {})

@login_required
def deleteConversation(request, conversationID):
	if ConversationLog.objects.filter(id=conversationID).exists():
		conversationToDelete = ConversationLog.objects.get(id=conversationID)
		conversationToDelete.delete()
	return HttpResponseRedirect('/private_messages/') 
