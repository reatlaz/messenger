from django.core.mail import EmailMessage
from django.utils import timezone
from users.models import User, UsersLastMonth
from chats.models import ChatMember, Chat

from dateutil.relativedelta import relativedelta

from application.celery import app


@app.task()
def add_together(a, b):
    return a + b


@app.task()
def update_unique_users():
    last_month = timezone.now().today() - relativedelta(months=5)
    res = User.objects.filter(date_joined__gt=last_month)
    users_last_month = UsersLastMonth.objects.get_or_create(pk=1)[0]
    users_last_month.number = len(res)
    users_last_month.save()





@app.task()
def send_email(message_body, chat_id):
    emails = []
    chat_name = Chat.objects.get(id=chat_id).name
    admins = ChatMember.objects.filter(chat_id=chat_id, role='admin').values('user__email')
    for admin in admins:
        emails.append(admin['user__email'])
    if emails:
        msg = EmailMessage(
            'New user added to chat',
            f'New user {message_body} has been added to chat {chat_name}',
            'm3sseng3r@yandex.ru',
            emails
        )
        msg.send()
