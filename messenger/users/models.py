from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=30) #откатить миграции, добавить AuthUserModel
    last_name = models.CharField(max_length=30)
    email = models.EmailField()