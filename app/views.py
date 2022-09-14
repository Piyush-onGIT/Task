from http.client import HTTPResponse
import re
from sre_constants import SUCCESS
from django.shortcuts import render
from flask import request
import crud
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def error_404_view(request, exception):
    return render(request, '404.html')

def home(request):
    cook = request.COOKIES
    if cook:
        try:
            if cook['login'] == '1':
                return render(request, "welcome.html", {"name": cook["name"]})
            else:
                return render(request, "index.html")
        except:
            return render(request, "index.html")
    else:
        return render(request, "index.html")

def signup(request):
    d = request.POST
    fname = d['fname']
    usnm = d['usnm']
    mail = d['email']
    passd = d['pswd']
    repass = d['rpswd']

    if ((not fname) or (not usnm) or (not mail) or (not passd) or (not repass)):
        return render(request, "index.html")

    if (passd != repass):
        # unmatched password
        messages.info(request, 2)
        return render(request, "index.html")

    check1 = crud.check_username(usnm)
    check2 = crud.check_mail(mail)

    if check1:
        # username exists
        messages.info(request, 1)
        return render(request, "index.html")
    
    if check2:
        # email exists
        messages.info(request, 3)
        return render(request, "index.html")

    crud.addUser(usnm, fname, mail, passd)
    
    # signup successfull
    messages.info(request, 7)
    return render(request, "index.html")

def loggedIN(request):
    data = request.POST
    usnm = data['usnm']
    name = crud.getName(usnm)[0]
    return render(request, "welcome.html", {"name": name})

def login(request):
    data = request.POST
    usnm = data['usnm']
    passd = data['pswd']

    if ((not usnm) or (not passd)):
        return render(request, "index.html")

    check = crud.check_username(usnm)

    if check:
        if check == passd:
            # logged in
            # messages.info(request, 4)
            name = crud.getName(usnm)[0]
            mail = crud.getName(usnm)[1]
            response = loggedIN(request)

            response.set_cookie("login", 1)
            response.set_cookie("name", name)
            response.set_cookie("username", usnm)
            response.set_cookie("email", mail)
            return response
        else:
            # wrong password
            messages.info(request, 5)
            return render(request, "index.html")
    else:
        # no account
        messages.info(request, 6)
        return render(request, "index.html")

    return render(request, "index.html")

def logout(request):
    response = render(request, "index.html")
    response.delete_cookie("login")
    response.delete_cookie("name")
    response.delete_cookie("email")
    response.delete_cookie("username")
    return response

def change(request):
    d = request.POST
    cook = request.COOKIES

    usnm = cook['username']
    name = cook['name']
    old = d['opswd']
    new = d['pswd']
    rep = d['rpswd']

    if (new != rep):
        messages.info(request, 8)
        return render(request, "welcome.html", {"name": name})

    else:
        if crud.changePwd(usnm, old, new):
            return logout(request)
        else:
            messages.info(request, 7)
            return render(request, "welcome.html", {"name": name})

def delete(request):
    username = (request.COOKIES)['username']
    crud.delete(username)
    return render(request, "index.html")