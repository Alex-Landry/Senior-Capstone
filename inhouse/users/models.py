from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    is_student = models.BooleanField(default=True)
    is_helper = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
