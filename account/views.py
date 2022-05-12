from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,"You have been registered successfully!")
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request,"account/register.html",{
        'form':form
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been loggedin successfully!")
            return redirect("/")
        else:
            messages.error(request,'Something went wrong please try again later')
            return redirect("/account/login")
    return render(request,"account/login.html")

def user_logout(request):
    logout(request)
    messages.success(request,"Loggedout successfully!")

    return redirect("/account/login")
