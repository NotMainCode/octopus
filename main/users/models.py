"""Database settings of the 'Users' app."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.MAX_LENGHT_USER_MODEL,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.MAX_LENGHT_USER_MODEL,
        blank=False,
    )
    email = models.EmailField(
        verbose_name="Почта",
        max_length=settings.MAX_LENGHT_USER_MODEL,
        blank=False,
        unique=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
