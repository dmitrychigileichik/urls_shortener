from django.contrib import admin
from .models import Shortener


class UrlshortenerAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'times_followed', 'long_url', 'short_url')


admin.site.register(Shortener, UrlshortenerAdmin)
