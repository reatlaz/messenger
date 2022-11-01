from django.db import models
from django.contrib.auth.models import AbstractUser

#сделать другие поля (др, о себе, статус, аватарку)
class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()