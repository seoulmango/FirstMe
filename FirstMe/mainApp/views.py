from django.shortcuts import render, redirect
from .models import Card, Groups, Friendlists
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    pass

def login(request):
    pass

def signup(request):
    pass

def make(request):
    pass

def detail(request):
    pass

def edit(request):
    pass




def group_detail(request):
    pass

def personal_invitation(request):
    pass

@login_required(login_url="/registration/login")
def group_invitation(request):
    pass

def group_list(request):
    pass

def friend_list(request):
    pass
