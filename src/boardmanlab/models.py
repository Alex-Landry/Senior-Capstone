from django.db import models

# Create your models here.


class user(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=50)

