from django.contrib import admin

from .models import Image, Topic, Chapter, Blitz

# Register your models here.
admin.site.register(Image)
admin.site.register(Topic)
admin.site.register(Chapter)
admin.site.register(Blitz)