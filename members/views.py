import logging

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from members.models import CustomUser



# Create your views here.
def loginUser(request):
    if request.method == "POST":
        logging.warning("POST block")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        logging.warning(user)
        if user is not None:
            login(request, user)
            return redirect("post_list")
            # Redirect to a success page.

        else:
            messages.error(request,"Credential not valid")
            logging.warning("non loggato")
            return redirect("loginUser")
    else:
        return render(request,'authentication/login.html',{})

def newUser(request):
    if request.method == "POST":
        logging.warning("POST block")
        username = request.POST["username"]
        password = request.POST["password"]
        file = request.FILES["avatar"]
        user = CustomUser.objects.filter(username=username)

        if user.count() == 0:
            CustomUser.objects.create_user(username=username,email="lennon@thebeatles.com", password=password,photo=file)
            return redirect("post_list")
            #CustomUser = CustomUser.object.create()
            # Redirect to a success page.

        else:
            messages.error(request,"Username already exists")
            logging.warning("user esistente")
            return redirect("newUser")
    else:
        return render(request, 'newUser.html', {})

def logoutUser(request):
    logout(request)
    return redirect("loginUser")

def resetPassword(request):
    if request.method == "POST":
        logging.warning("resetPassword")
        
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            u = CustomUser.objects.get(username=username)
            u.set_password(password)
            u.save()
        except:
            logging.warning("problema reset passwrod")
            messages.error(request,"Problem reset password")
            return redirect("resetPassword")
    else:
        return render(request,'reset_password.html',{})
    return redirect("loginUser")
