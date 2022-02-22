from django.db import models
from users import models as u
# Create your models here.

class helpSession(models.Model):
    helper = models.ForeignKey(u.User, on_delete=models.CASCADE)
    subject = models.TextField(max_length=300)
    date = models.DateField()
    duration = models.IntegerField(default=30)
    topic = models.TextField(max_length=300)
    attendance = models.IntegerField(default=0)