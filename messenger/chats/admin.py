from django.contrib import admin

from .models import Chat, Message, ChatMember
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")


class MessageAdmin(admin.ModelAdmin):
    ordering = ("created_at",)


admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatMember)