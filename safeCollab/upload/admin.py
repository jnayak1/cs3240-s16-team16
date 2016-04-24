from django.contrib import admin

# Register your models here.
from .forms import SignUpForm, UploadFileForm, PublicKeyForm
from .models import SignUp, PublicKey

class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp", "updated"]
    form = SignUpForm
#    class Meta:
 #       model = SignUp

# class UploadFileAdmin(admin.ModelAdmin):
#     list_display = ["__str__"]
#     form = UploadFileForm

class PublicKeyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "key"]
    form = PublicKeyForm

admin.site.register(SignUp, SignUpAdmin)
#admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(PublicKey, PublicKeyAdmin)
