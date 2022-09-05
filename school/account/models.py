import datetime
import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User, Group


class TokenLogin(models.Model):
    objects = models.Manager()
    token = models.CharField(max_length=255, null=False, unique=True)
    user = models.ForeignKey(User, related_name='TokenLogins', null=False, on_delete=models.CASCADE)


class Player(models.Model):
    default_group = Group.objects.filter(name='ELEVE').first().pk

    objects = models.Manager()
    confirm = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='Players', null=False, on_delete=models.CASCADE)
    prev_group = models.ForeignKey(Group, related_name='Players', null=False, on_delete=models.CASCADE, default=default_group)
