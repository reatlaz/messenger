from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    avatar = models.ImageField(blank=True)
    bio = models.CharField(max_length=500, default="")
    status = models.CharField(max_length=20, null=True)
    birth_date = models.DateField(blank=True, null=True)
    last_seen = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.pk) + ' ' + str(self.username)
