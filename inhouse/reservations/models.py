from django.db import models
from boardmanlab.models import helpSession
from users.models import User

# Create your models here.
class Reservation(models.Model):
    helpSession =  models.ForeignKey(helpSession, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
