from django.contrib import admin

# Register your models here.


from users.models import Topic
from .models import helpSession
from reservations.models import Reservation

class TopicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Topic, TopicAdmin)

admin.site.register(helpSession, TopicAdmin)
admin.site.register(Reservation, TopicAdmin)

