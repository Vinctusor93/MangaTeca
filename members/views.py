import logging

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
#from members.models import CustomUser



# Create your views here.
def loginUser(request):
    if request.method == "POST":
        logging.warning("POST block")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("post_list")
            # Redirect to a success page.

        else:
            messages.error(request,"Credential not valid")
            logging.warning("non loggato")
            return redirect("login")
    else:
        return render(request,'authentication/login.html',{})

def newUser(request):
    if request.method == "POST":
        logging.warning("POST block")
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.filter(username=username)

        if user.count() == 0:
            User.objects.create_user(username, password)
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
    return redirect("login")