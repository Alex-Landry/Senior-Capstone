import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_helper = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email
        return user