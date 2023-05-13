from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.

def login(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            django_login(request,user=user)
            return redirect("index")
        else:
            messages.add_message(request, messages.ERROR,"Invalid Credentials")
            return render(request,'account/login.html',{})
    else:
        return render(request,'account/login.html',{})



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        u = User.objects.create(username=username,email=email)
        u.set_password(password1)
        u.save()
        return redirect("register_done")
    else:
        return render(request,'account/register.html',{})

def logout(request):
    django_logout(request)
    return redirect('logout_done')