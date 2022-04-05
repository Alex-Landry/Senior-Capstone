from django.contrib import admin

# Register your models here.


from users.models import Topic
from .models import helpSession
from reservations.models import Reservation


class BoardmanAdmin(admin.ModelAdmin):
    pass




admin.site.register(helpSession, BoardmanAdmin)
admin.site.register(Reservation, BoardmanAdmin)
