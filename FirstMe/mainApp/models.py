from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    link = models.TextField()
    invitation_link = models.IntegerField(null=True)

# 친구 목록 모델을 아예 따로 만들어서, 그 목록의 주인 값을 받는 형식으로 만들어봤어.
class Friendlists(models.Model):
    me = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="friendlist" )
    friends = models.ManyToManyField(Card)

# 서버에 존재하는 모든 그룹들. (각 그룹 페이지에 들어갈 수 있는 유저는 그룹의 members 뿐이다.)
class Groups(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owning")
    name = models.CharField(max_length=30)
    # 그 그룹에 속해 있는 카드들의 관계를 보여주는 members
    members = models.ManyToManyField(Card)
    invitation_link = models.IntegerField(null=True)