from django.db import models
from users.models import User
# ManyToMany -> ChatMember
# users - нет
# описание, ад

class Chat(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.name) + ', ' + str(self.users)


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

    def __str__(self):
        return self.chat, self.sender, self.recieved_date
        
class ChatMember(models.Model):
    user = ForeignKey()
    chat = ForeignKey()
    date_joined()
    