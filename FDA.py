from tkinter import *
from tkinter import filedialog
import httplib2, urllib
import requests
import re
import pickle
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
from Crypto import Random
import binascii
import os

stayLogged = 0
key = ""
username = ""
currentDir = ""
encryptFile = False

class Login:

    def __init__(self, master):
        self.master = master

        self.frame = Frame(master, width = 600, height = 300)
        self.frame.pack(side=TOP)
        label1 = Label(self.frame, text="Username")
        label2 = Label(self.frame, text="Password")
        self.entry1 = Entry(self.frame)
        self.entry2 = Entry(self.frame)

        label1.grid(row=0, sticky=E)
        label2.grid(row=1, sticky=E)

        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)

        c = Checkbutton(self.frame, text="Keep me logged in", command=self.remember)
        c.grid(row=2, column=0, columnspan=2)

        submit = Button(self.frame, text="Login", width=10, command=self.submitLogin)
        submit.grid(row=3, columnspan=2)

        self.info = Label(self.frame, text="")
        self.info.grid(row = 4, columnspan = 2)

    def submitLogin(self):
        global key
        global username
        global stayLogged
        username = self.entry1.get()
        password = self.entry2.get()
        test = requests.get("http://127.0.0.1:8000/external/" + username + "/" + password)
        key = test.text
        #Take out the quotes from the http response
        key = re.sub('["]', '', key)
        print(key)
        if not key == "Invalid login details supplied.":
            global currentDir
            global stayLogged
            currentDir = os.path.dirname(__file__)
            loginFile = os.path.join(currentDir, "loginInfo.txt")
            if stayLogged:
                with open(loginFile, 'w+') as loginInfo:
                    loginInfo.write(username + '\n')
                    loginInfo.write(key + '\n')
            self.frame.pack_forget()
            self.window = MainWindow(self.master)
        else:
            self.info['text'] = "Invalid login details supplied."

    def remember(self):
        global stayLogged
        stayLogged = not stayLogged


def encrypt_file(input_file, input_file_path):
    deskey = Random.get_random_bytes(20)
    iv = deskey[0:8]
    key_16 = deskey[0:16]
    file_name_enc = input_file + ".enc"
    des = DES3.new(key_16, DES3.MODE_CFB, iv)
    if os.path.isfile("keys.p"):
        file_key_dict = pickle.load(open("keys.p", "rb"))
        print(str(key_16))
        print(input_file)
        file_key_dict.update({input_file: key_16})
        pickle.dump(file_key_dict, open("keys.p", "wb"))
    else:
        print(input_file)
        print(str(key_16))
        file_key_dict = {input_file: key_16}
        pickle.dump(file_key_dict, open("keys.p", "wb"))
    with open(file_name_enc, 'wb+') as output:
        with open(input_file_path, 'rb+') as input:
            while True:
                chunk = input.read(16)
                if not chunk:
                    break
                output.write(des.encrypt(chunk))
            return True
        return True
    return False

def decrypt_file(name, input_file):
    if os.path.isfile("keys.p"):
        file_key_dict = pickle.load(open("keys.p", "rb"))
        # des = file_key_dict.get(name)
        deskey = file_key_dict.get(name)
        if not deskey == None:
            iv = deskey[0:8]
            key_16 = deskey[0:16]
            print(str(key_16))
            des = DES3.new(key_16, DES3.MODE_CFB, iv)
            # print(str(des))
            # with open(name, 'wb') as fd:
            #     for chunk in input_file.iter_content(chunk_size=16):
            #         print(des.decrypt(chunk))
            #         fd.write(des.decrypt(chunk))
            with open('decrypter', 'wb+') as information:
                information.write(input_file.raw.read())
            # i = 0
            # with open(name, 'wb+') as output:
            #     while i < len(input_file)+16:
            #         chunk = input_file[i:i+16]
            #         print(des.decrypt(chunk))
            #         output.write(des.decrypt(chunk))
            #         i+=16
            #     return True
            # return False
                # with open(file_name_enc, 'wb+') as output:

            with open(name, 'wb+') as output:
                with open('decrypter', 'rb+') as input:
                    while True:
                        chunk = input.read(16)
                        if not chunk:
                            break
                        # print("It makes it here...")
                        output.write(des.decrypt(chunk))
                        # print(des.decrypt(chunk).decode())
                    return True
            return False
        else:
            print("You do not have the key to this file")
            return False
    else:
        print("You have no symmetric keys")
        return False

class MainWindow(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.frame = Frame(master, width=300, height=300)
        self.frame.pack(side=TOP)

        global encryptFile
        encryptFile = False

        logout_button = Button(self.frame, text='Logout', command=self.logout)
        logout_button.grid(row=0, column=1, sticky=E)

        title = Label(self.frame, text="View Reports")
        title.grid(row=1, columnspan=4)

        label3 = Label(self.frame, text="Choose Report:")
        label3.grid(row=2)

        self.listbox = Listbox(self.frame)
        self.listbox.bind('<<ListboxSelect>>', self.seeReport)
        self.listbox.grid(padx=10, row=2, column = 1)

        self.getReports()

        separator = Label(self.frame, text="-----------------------------------------------")
        separator.grid(row=3, columnspan=4)

        label1 = Label(self.frame, text="File Upload")
        label2 = Label(self.frame, text="Choose File:")

        label1.grid(row=4, columnspan=4)
        label2.grid(row=5, column=0, sticky=E)

        browseFilesButton = Button(self.frame, text='Browse', width=15, command=self.upload)
        browseFilesButton.grid(row=5, column=1)

        c = Checkbutton(self.frame, text="Encrypt the file", command=self.encrypt)
        c.grid(row=6, columnspan = 2)

    def seeReport(self, evt):
        if not self.listbox.size() == 0:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            # print('You selected item %d: "%s"' % (index, value))
            # print(self.listbox.get(self.listbox.curselection()))
            url = "http://127.0.0.1:8000/external/seeReport/"
            url = url + username + "/" + value
            response = requests.get(url).text
            #print(response)
            self.frame.pack_forget()
            self.window = Report(self.master, response)

    def getReports(self):
        global key
        global username
        url = "http://127.0.0.1:8000/external/GetReports/"
        url = url + username + "/" + key
        response = requests.get(url).text
        print(response)
        if not response == None:
            reports = json.loads(response)
            counter = 0
            for value in reports.values():
                self.listbox.insert(END, value)
        else:
            print("You don't have access to any reports.")

    def upload(self):
        global encryptFile
        if encryptFile:
            file_path = filedialog.askopenfilename()
            file_path_dirs = file_path.split("/")
            file_name = file_path_dirs[len(file_path_dirs) - 1]
            file_path_dirs = file_name.split("\\")
            file_name = file_path_dirs[len(file_path_dirs) - 1]
            encrypt_file(file_name, file_path)
            print(os.path.dirname(__file__))
            print(file_path)
            url = "http://127.0.0.1:8000/external/receiveFile/"
            url = url + username + "/" + key + "/" + file_name + '/' + str(encryptFile)
            # print("This is the url to put the file on the database:")
            # print(url)
            # print(file_name + '.enc')
            # print("This is what we should be decrypting:")
            # with open(file_path+".enc", 'rb') as test:
            #     print(test.read())
            # os.path.normpath(os.path(file_name+".enc"))
            r = requests.post(url, files={file_name: open(file_name + ".enc", 'rb')})
            print(r.text)
            if os.path.isfile(file_name + ".enc"):
                os.remove(file_name + ".enc")
            #print(r.text)
        else:
            file_path = filedialog.askopenfilename()
            file_path_dirs = file_path.split("/")
            file_name = file_path_dirs[len(file_path_dirs) - 1]
            file_path_dirs = file_name.split("\\")
            file_name = file_path_dirs[len(file_path_dirs) - 1]
            url = "http://127.0.0.1:8000/external/receiveFile/"
            url = url + username + "/" + key + "/" + file_name + "/" + str(encryptFile)
            # print(url)
            # print(file_name)
            # with open(file_path, 'rb') as test:
            #     print(test.read())
            r = requests.post(url, files={file_name: open(file_path, 'rb')})

    def encrypt(self):
        global encryptFile
        encryptFile = not encryptFile

    def logout(self):
        global stayLogged
        stayLogged = 0
        loginFile = os.path.join(currentDir, "loginInfo.txt")
        if os.path.isfile(loginFile):
            os.remove(loginFile)
        url = "http://127.0.0.1:8000/external/logout/"
        url = url + key
        # print(url)
        print(requests.get(url).text)
        self.frame.pack_forget()
        self.window = Login(self.master)


class Report:

    def __init__(self, master, info):
        self.master = master

        report = json.loads(info)

        self.frame = Frame(master, width = 600, height = 300)
        self.frame.pack(side=TOP)

        logout_button = Button(self.frame, text='Logout', command=self.logout)
        logout_button.grid(row=0, column=1, sticky=E)

        home_button = Button(self.frame, text='Home', command=self.goMain)
        home_button.grid(row=0, column=0, sticky=W)

        title = Label(self.frame, text="Report Title: " + report.get("Title"))
        title.grid(row=1, columnspan = 2)
        owner = Label(self.frame, text="Owner: " + report.get("Owner"))
        owner.grid(row=2, columnspan = 2)

        shortDescription = Label(self.frame, text="Short Description: " + report.get("Short"), wraplength=275, justify=LEFT)
        shortDescription.grid(row=3, columnspan = 2)

        # key_label = Label(self.frame, text="Key:")
        # self.key_entry = Entry(self.frame)
        # key_label.grid(row=3, sticky=W)
        # self.key_entry.grid(row=3)

        files = Label(self.frame, text="Files, click to download:", wraplength=200)
        files.grid(row=5, columnspan = 2)
        self.listbox = Listbox(self.frame)
        self.listbox.bind('<<ListboxSelect>>', self.getFile)
        self.listbox.grid(padx=10, row=6, columnspan = 2)
        for value in report["Files"]:
            self.listbox.insert(END, value)

        longDescription = Label(self.frame, text="Long Description: " + report.get("Long"), wraplength=275, justify=LEFT)
        longDescription.grid(row=7, columnspan = 2)

    def getFile(self, evt):
        if not self.listbox.size() == 0:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            url = "http://127.0.0.1:8000/external/getFile/"
            url = url + username + "/" + value
            # print("This is the url for getting the file:")
            # print(url)
            response = requests.get(url, stream=True)
            suffix = value[len(value)-4:len(value)]
            if suffix == ".enc":
                # print(value[0:len(value)-4])
                # print('This is what we are actually decrypting:')
                # print(response.raw.read())
                decrypt_file(value[0:len(value)-4], response)
                if os.path.isfile('decrypter'):
                    os.remove('decrypter')
            else:
                # print(suffix)
                # with open(value, 'wb+') as output:
                #     output.write(bytes(response.text, "UTF-8"))
                with open(value, 'wb+') as information:
                    information.write(response.raw.read())
        else:
            print("There are no files in this report")

    def goMain(self):
        self.frame.pack_forget()
        self.window = MainWindow(self.master)

    def logout(self):
        global stayLogged
        stayLogged = 0
        loginFile = os.path.join(currentDir, "loginInfo.txt")
        if os.path.isfile(loginFile):
            os.remove(loginFile)
        url = "http://127.0.0.1:8000/external/logout/"
        url = url + key
        # print(url)
        print(requests.get(url).text)
        self.frame.pack_forget()
        self.window = Login(self.master)

def doNothing():
    print("I'm doing nothing!")

#Destroy user's ad hoc 'session' when the window is closed (if stayLogged = 0)
def _delete_window():
    print("delete_window")
    try:
        global stayLogged
        if not stayLogged:
            global key
            if not (key == "" or key == "Invalid login details supplied."):
                #Destroy the user's ad hoc "session" if it exists
                url = "http://127.0.0.1:8000/external/logout/"
                url = url + key
                # print(url)
                print(requests.get(url).text)
        root.destroy()
    except:
        pass

def checkLoginInfo():
    global currentDir
    global username
    global key
    global stayLogged
    currentDir = os.path.dirname(__file__)
    loginFile = os.path.join(currentDir, "loginInfo.txt")
    if os.path.isfile(loginFile):
        with open(loginFile, 'r+') as loginInfo:
            username = loginInfo.readline().replace('\n', '')
            key = loginInfo.readline().replace('\n', '')
        url = "http://127.0.0.1:8000/external/verifyUser/"
        url = url + username + "/" + key
        # print(url)
        session = requests.get(url).text
        #Take out the quotes from the http response
        session = re.sub('["]', '', session)
        # print(session)
        if session == "You have an active session.":
            stayLogged = 1
            window = MainWindow(root)
        else:
            os.remove(loginFile)
            login = Login(root)
    else:
        login = Login(root)

#Creates a main window
root = Tk()
root.geometry('{}x{}'.format(300, 420))

root.protocol("WM_DELETE_WINDOW", _delete_window)

checkLoginInfo()

#Displays the main window
root.mainloop()