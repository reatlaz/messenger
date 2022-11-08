from django.db import models
from users.models import User


class Chat(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500, default="")
    picture = models.ImageField(null=True)

    def __str__(self):
        return f'{self.pk} "{self.name}"'


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='member')

    def __str__(self):
        return f'id: {self.pk}, user: {self.user}, chat: {self.chat}, role: {self.role}'


class Message(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_forwarded = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        ChatMember,
        null=True,
        on_delete=models.SET_NULL,
        related_name="chat_messages")

    # class Meta:
    #     verbose_name_plural

    def __str__(self):
        return f'{self.id} "{self.content}" created at {self.created_at} | CHAT: {self.chat} | SENDER: {self.sender}'
