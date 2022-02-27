import email
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class Topic(models.Model):
    topic = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ['topic']

    def __str__(self):
        return self.topic


class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_helper = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    picture = models.TextField(null=True, blank=True)
    topics = models.ManyToManyField(Topic)
    


    

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email
        user.picture = sociallogin.account.extra_data['picture']
        return user