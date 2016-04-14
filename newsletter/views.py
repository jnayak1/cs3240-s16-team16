from django.shortcuts import render
from .forms import SignUpForm, UploadFileForm, PublicKeyForm
from .models import PublicKey
from django.http import HttpResponseRedirect

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
from Crypto import Random
import binascii
import os


def home(request):
    title = "Form uploading"
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.full_name:
            instance.full_name = "No name"
        instance.save()
        print(instance)
    context = {
        "title": title,
        "form": form,
    }
    return render(request, "home.html", context)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request.POST["name"])
            return HttpResponseRedirect('success')
        else:
            return HttpResponseRedirect('failure')
    else:
        form = UploadFileForm();
        context = {
            "form" : form,
        }
        return render(request, "upload.html", context)


def handle_uploaded_file(f, n):
    name, fileType = f.name.split(".")
    encrypt_file(f, n)


def uploaded(request):
    if request.method == 'POST':
        decrypt_file(request.POST['file'])
        blankform = PublicKeyForm()
        context={
            "form" : blankform,
        }
        return render(request, "success.html", context)
    else:
        blankform = PublicKeyForm()
        context={
            "form" : blankform,
        }
        return render(request, "success.html", context)


def failed(request):
    return render(request, "failure.html", {})


def encrypt_file(input_file, n):
    deskey = Random.get_random_bytes(20)
    iv = deskey[0:8]
    key_16 = deskey[0:16]
    des = DES3.new(key_16, DES3.MODE_CFB, iv)
    name, fileType = input_file.name.split(".")
    file_name = n + "." + fileType + ".enc"
    file = "media/" + file_name
    stored_key = PublicKeyForm({"file" : file_name, "key" : binascii.hexlify(key_16)})
    if stored_key.is_valid():
        stored_key.save()
    else:
        print(stored_key.errors)
    with open(file, 'wb+') as output:
        for chunk in input_file.chunks(16):
            output.write(des.encrypt(chunk))
        return True
    return False


def decrypt_file(input_file):
    file_info = PublicKey.objects.all().filter(file=input_file)[0]
    print(file_info)
    #print(len(file_info))
    key = binascii.unhexlify(file_info.key)
    if os.path.isfile("media/" + input_file):
        iv = key[0:8]
        key_16 = key[0:16]
        des = DES3.new(key_16, DES3.MODE_CFB, iv)
        name, fileType, enc = input_file.split(".")
        with open("media/" + name + "." + fileType, 'wb+') as output:
            with open("media/" + input_file, 'rb+') as input:
                while True:
                    chunk = input.read(16)
                    if not chunk:
                        break
                    output.write(des.decrypt(chunk))
                return True
        return False
    else:
        print("It can't find the file")
        return False
    # return False
