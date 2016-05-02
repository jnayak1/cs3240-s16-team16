from django.contrib import admin
from private_messages.models import Message, ConversationLog

class MessageAdmin(admin.ModelAdmin):
	pass

class ConversationLogAdmin(admin.ModelAdmin):
	pass

admin.site.register(Message, MessageAdmin)
admin.site.register(ConversationLog, ConversationLogAdmin)