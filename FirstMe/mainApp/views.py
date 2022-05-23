from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from .models import Card, Groups, Friendlists
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random

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

@login_required(login_url="/registration/login")
def group_detail(request, group_pk):
    group = Groups.objects.filter(pk=group_pk)
    user = request.user
    if user in group.members:
        return render(request, "group_detail.html")
    else:
        error = "이 그룹의 열람 권한이 없습니다."
        return render(request, "group_detail.html", {
            'error': error
        })


# def personal_invitation(request):
#     pass

@login_required(login_url="/registration/login")
def make_group(request):
    if request.method == "POST":
        name = request.POST["name"]

        # 동일한 invitation_link를 가진 그룹이 있는가?
        while True:
            new_code = random.randrange(0, 2000000000)
            already = Groups.objects.filter(invitation_link = new_code)
            if not already:
                break
            else:
                continue

        new_group = Groups.objects.create(
            name=name,
            creater=request.user,
            invitation_link=new_code
            )
        return redirect('group_invitation', new_group.pk, new_group.invitation_link)
    return render(request, "make_group.html")

@login_required(login_url="/registration/login")
def group_invitation(request, group_pk, access_code):
    group = Groups.objects.filter(pk=group_pk)
    user = request.user
    # 사이트에 입장한 유저 그룹 멤버에 추가하기
    group.members.add(user)

    # 관리자가 QR코드 닫기 버튼 눌렀을 때, 공유 링크 닫기
    if request.method == "POST":
        group.update(invitation_link=None)
        return render(request, "group_detail.html", {
        'user': user,
        'group': group,
        })

    return render(request, "group_invitation.html", {
        'user': user,
        'group': group
    })


# def group_list(request):
#     pass

# def friend_list(request):
#     pass