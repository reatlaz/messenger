# Generated by Django 4.1.2 on 2022-10-18 19:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0003_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]