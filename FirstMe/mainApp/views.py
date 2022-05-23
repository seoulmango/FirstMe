from django.shortcuts import render, redirect
from .models import Card, Groups, Friendlists
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

# def home(request):
#     pass

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        found_user = User.objects.filter(username=username)
        if found_user:
            error = "이미 아이디가 존재합니다"
            return render(request, 'registration/signup.html', {
                'error': error,
            })
        new_user = User.objects.create_user(
            username = username,
            password = password
        )
        auth.login(request,new_user)
        return redirect('home')
    return render(request, 'registration/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(request.GET.get("next", "/"))
        error = "아이디나 비번이 틀립니다"
        return render(request, 'registration/login.html', {
            'error': error,
        })
    return render(request, "registration/login.html")

# def make(request):
#     pass

# def detail(request):
#     pass

# def edit(request):
#     pass




# def group_detail(request):
#     pass

# def personal_invitation(request):
#     pass

def make_group(request):
    if request.method == "POST":
        name = request.POST["name"]
        new_group = Groups.objects.create(name=name)
    return render(request, "make_group.html")

# @login_required(login_url="/registration/login")
# def group_invitation(request):
#     # 로그인된 유저를 user로 받기.
#     pass

# def group_list(request):
#     pass

# def friend_list(request):
#     pass