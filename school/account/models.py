import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User


class TokenLogin(models.Model):
    objects = models.Manager()
    token = models.CharField(max_length=255, null=False, unique=True)
    user = models.ForeignKey(User, related_name='TokenLogins', null=False, on_delete=models.CASCADE)


class Player(models.Model):
    objects = models.Manager()
    confirm = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='Players', null=False, on_delete=models.CASCADE)
