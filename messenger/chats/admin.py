from django.contrib import admin

from .models import Chat, Message
# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)


class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")
