from django.db import models
from users import models as u

# Create your models here.


class helpSession(models.Model):
    helper = models.ForeignKey(u.User, on_delete=models.CASCADE)
    topic = models.TextField(max_length=300)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(default=30)
    attendance = models.IntegerField(default=0, blank=True, null=True)
    is_remote = models.BooleanField(default=False, blank=False, null=True)
    is_inperson = models.BooleanField(default=True, blank=False, null=True)
    remote_link = models.URLField(max_length=200, blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        ordering = ["time"]
