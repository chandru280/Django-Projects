from django.contrib import admin

from .models import *


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('user', 'to', 'body', 'created_at')
    search_fields = ('to', 'body', 'user__username')
    list_filter = ('created_at',)