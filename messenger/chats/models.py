from django.db import models
from users.models import User


class Chat(models.Model):
    name = models.CharField(verbose_name='название', max_length=30)
    description = models.CharField(verbose_name='описание', max_length=500, default="")
    picture = models.ImageField(verbose_name='картинка', null=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f'{self.pk} "{self.name}"'


class ChatMember(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, verbose_name='чат', on_delete=models.CASCADE)
    role = models.CharField(verbose_name='роль', max_length=20, default='member')

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чатов'

    def __str__(self):
        return f'member_id: {self.pk}, user: {self.user}, chat: {self.chat}, role: {self.role}'


class Message(models.Model):
    content = models.CharField(verbose_name='', max_length=500)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True, blank=True)
    is_forwarded = models.BooleanField(verbose_name='переслано', default=False)
    is_read = models.BooleanField(verbose_name='прочитано', default=False)
    chat = models.ForeignKey(Chat, verbose_name='чат', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        ChatMember,
        verbose_name='отправитель',
        null=True,
        on_delete=models.SET_NULL,
        related_name="chat_messages")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.id} "{self.content}" created at {self.created_at} | CHAT: {self.chat} | SENDER: {self.sender}'

    def get_chat(self):
        chat = self.chat
        full_chat = f'{chat.id} "{chat.name}"'
        return full_chat
