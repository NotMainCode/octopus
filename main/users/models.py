"""Database settings of the 'Users' app."""

from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models

from main.settings import MAX_LENGHT_USER_MODEL


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="Имя", max_length=MAX_LENGHT_USER_MODEL, blank=False, null=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=MAX_LENGHT_USER_MODEL, blank=True, null=False
    )
    email = models.EmailField(
        verbose_name="Почта", max_length=MAX_LENGHT_USER_MODEL, blank=True, null=False
    )
