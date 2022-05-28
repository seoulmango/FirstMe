from django.shortcuts import render, redirect
from .models import Card, Groups, Friendlists
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
import qrcode
from PIL import Image

# Create your views here.

    

def home(request):
    user = request.user
    if user.is_authenticated:
        card = Card.objects.get(owner=user)
        return render(request, 'home.html', {
        'user':user,
        'card':card,
        })
    return render(request, 'home.html', {
        'user':user,
        })

def signup(request):
    if request.method == "POST":
        # 도메인을 벌써 소유한 다른 카드가 있는가?
        link = request.POST['link']
        found_link = Card.objects.filter(link = link)
        username = request.POST['username']
        password = request.POST['password']
        found_user = User.objects.filter(username=username)

        if found_link:
            error = "같은 도메인의 소유자가 벌써 있습니다"
            return render(request, 'registration/signup.html', {
                'error': error,
            })
        
        # 겹치는 아이디가 있는가?
        elif found_user:
            error = "이미 아이디가 존재합니다"
            return render(request, 'registration/signup.html', {
                'error': error,
            })
        
        # 도메인&아이디가 배타적일 때 새 명함&계정 만들기
        else:
            new_user = User.objects.create_user(
                username = username,
                password = password,
            )

            auth.login(request,new_user)

            user = request.user
            name = request.POST['name']
            phone_num = request.POST['phone_num']
            link = request.POST['link']
            intro = request.POST['intro']
            mbti = request.POST['mbti']
            profile_pic = request.POST['profile_pic']

            
            new_card = Card.objects.create(
                owner = user,
                link = link,
                name=name,
                phone_num=phone_num,
                intro=intro,
                mbti=mbti,
                )
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
    # 유저가 벌써 명함을 소유하고 있는가?
    user = request.user
    # if user.cards:
    #     error = "벌써 명함이 있습니다"
    #     return render(request, 'make.html', {'error':error})

    if request.method=="POST":
        name = request.POST['name']
        user = request.user
        phone_num = request.POST['phone_num']
        link = request.POST['link']
        intro = request.POST['intro']
        mbti = request.POST['mbti']

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
    user = request.user
    card = Card.objects.get(link=card_link)
    # 이 명함의 주인일 때
    if card.owner == user:
        return render(request, "detail.html", {"card":card})
    # 방문 유저와 명함이 같은 그룹에 있을 때
    user_groups = user.mygroups.all()
    access = False

    for group in user_groups:
        members = group.members.all()
        if card.owner in members:
            access = True
    
    if access:
        return render(request, "detail.html", {"card": card})

    # 열람 권한이 없을 때
    else:
        error = "이 명함의 열람 권한이 없습니다."
        return render(request, "detail.html", {"error":error})


# def edit(request):
#     pass

@login_required(login_url="/registration/login")
def group_detail(request, group_pk):
    group = Groups.objects.get(pk=group_pk)
    user = request.user
    members = group.members.all()
    if user in members:
        return render(request, "group_detail.html", {
            'group': group,
            'user':user,
            'members': members
        })
    else:
        error = "이 그룹의 열람 권한이 없습니다."
        return render(request, "group_detail.html", {
            'error': error
        })

@login_required(login_url="/registration/login")
def group_list(request, card_link):
    user = request.user
    groups = user.mygroups.all()
    card = Card.objects.get(link=card_link)
    # 이 명함의 주인일 때
    if card.owner == user:
        return render(request, "group_list.html",{
            "card":card,
            'user':user,
            'groups':groups,
        })
    else:
        error = "이 명함 그룹의 열람 권한이 없습니다."
        return render(request, "group_list.html",{
            "error": error,
            "card":card,
            'user':user,
            'groups':groups,
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
    group = Groups.objects.get(pk=group_pk)
    user = request.user
    # 코드가 유효하면, 사이트에 입장한 유저 그룹 멤버에 추가하기
    if group.invitation_link == access_code:
        group.members.add(user)
        group.save()
    else:
        error = "이 그룹의 공유 코드가 닫혔습니다. 그룹장에게 문의해주세요."
        return render(request, "group_invitation.html", {
        'user': user,
        'group': group,
        'error': error
    })

    # 관리자가 QR코드 닫기 버튼 눌렀을 때, 공유 링크 닫기
    if request.method == "POST":
        group = Groups.objects.filter(pk=group_pk)
        group.update(invitation_link=None)
        group = Groups.objects.get(pk=group_pk)
        return redirect("group_detail", group_pk)

    # qr 코드 생성하여 띄우기

    img = qrcode.make('group/'+ str(group_pk)+'/'+ str(access_code)+'/')
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
    )
    qr.add_data('group/'+str(group_pk)+'/'+str(access_code)+'/')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save(str(access_code)+".png")
    return render(request, "group_invitation.html", {
        'user': user,
        'group': group,
        'img': img,
    })

# def friend_list(request):
#     pass