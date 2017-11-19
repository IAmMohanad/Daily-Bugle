from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import login, authenticate
import os
#from django.contrib.auth.forms import UserCreationForm

from .forms import SignUpForm

from django.contrib.auth.hashers import check_password, make_password

from .models import User
from .models import Category
from .models import Article
from .models import Comment
from .models import Like

from django.contrib.auth import authenticate

@csrf_exempt
@login_required
def index(request):
    #return HttpResponse("Hello, world. You're at the news index.")
    return render(request, 'news/index.html', {})

@csrf_exempt
def signup(request):
    if(request.method == "POST"):
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
        return render(request, 'news/registration/signup.html', {'form':form})

    if(request.method == "GET"):
        form = SignUpForm()

    return render(request, 'news/registration/signup.html', {'form':SignUpForm})

@csrf_exempt
def login(request):
    if(request.method == "GET"):
        return render(request, 'news/registration/login.html', {})
    if(request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)
        if(user is None):
            return render(request, 'news/registration/login.html', {'no_user':"Email does not exist"})
        else:
            return render(request, 'news/index.html', {})
