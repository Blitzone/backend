from django.contrib import admin

from .models import UserTopic, Topic, UserChapter, Chapter, Blitz

# Register your models here.
admin.site.register(UserTopic)
admin.site.register(Topic)
admin.site.register(Chapter)
admin.site.register(UserChapter)
admin.site.register(Blitz)