from django.shortcuts import render, redirect
from .models import Card, Groups, Friendlists
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

def home(request):
    user = request.user
    return render(request, 'home.html', {'user':user})

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

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url="/registration/login")
def make(request):
    if request.method=="POST":
        name = request.POST['name']
        user = request.user
        phone_num = request.POST['phone_num']
        link = request.POST['link']
        intro = request.POST['intro']
        mbti = request.POST['mbti']

        # 유저가 벌써 명함을 소유하고 있는가?
        # if len(user.cards):
        #     error = "벌써 명함이 있습니다"
        #     return render(request, 'make.html', {'error':error})

        # 도메인을 벌써 소유한 다른 카드가 있는가?
        already = Card.objects.filter(link = link)
        if len(already):
            error = "같은 도메인의 소유자가 벌써 있습니다"
            return render(request, 'make.html', {'error':error})
        else:
            new_card = Card.objects.create(
                owner = user,
                link = link,
                name=name,
                phone_num=phone_num,
                intro=intro,
                mbti=mbti,
                )
            return redirect('home')
    return render(request, "make.html")

@login_required(login_url="/registration/login")
def detail(request, card_link):
    card = Card.objects.filter(link=card_link)
    return render(request, "detail.html", {"card":card})

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
        return redirect('group_invitation', new_group.pk, new_code)
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
        return render(request, "group_detail.html", group_pk, {
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