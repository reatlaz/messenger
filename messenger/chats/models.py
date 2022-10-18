from django.db import models
from users.models import User

class Chat(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(User)


class Message(models.Model):
    content = models.CharField(max_length=500)
    recieved_date = models.DateField()
    is_forwarded = models.BooleanField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="chat_messages")
    