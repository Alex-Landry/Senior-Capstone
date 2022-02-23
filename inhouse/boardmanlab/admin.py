from django.contrib import admin

# Register your models here.


from users.models import Topic
from .models import helpSession

class TopicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Topic, TopicAdmin)

admin.site.register(helpSession, TopicAdmin)

