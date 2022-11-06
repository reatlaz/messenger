from django.db import models
from users.models import User


class Chat(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500, default="")
    picture = models.ImageField(null=True)


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)


class Message(models.Model):
    content = models.CharField(max_length=500)
    received_date = models.DateField(default=None)
    is_forwarded = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        ChatMember,
        null=True,
        on_delete=models.SET_NULL,
        related_name="chat_messages")

    def __str__(self):
        return self.chat, self.sender, self.received_date
        

    