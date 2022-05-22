from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    link = models.TextField()
    # friend_list = models.
    invitation_link = models.TextField(null=True)

class Group(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owning")
    name = models.CharField(max_length=30)
    # members = models.
    invitation_link = models.TextField(null=True)
