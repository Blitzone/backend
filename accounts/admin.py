from django.contrib import admin

# Register your models here.
from .models import BlitzUser, Notification

admin.site.register(BlitzUser)
admin.site.register(Notification)