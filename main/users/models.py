"""Database settings of the 'Users' app."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from users.model_fields import CustomEmailField
from users.user_manager import CustomUserManager
from users.validators import validate_first_name_and_last_name_fields


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.MAX_LEN_FULL_NAME_USER_MODEL,
        blank=False,
        validators=[validate_first_name_and_last_name_fields],
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.MAX_LEN_FULL_NAME_USER_MODEL,
        blank=False,
        validators=[validate_first_name_and_last_name_fields],
    )
    email = CustomEmailField(
        verbose_name="Почта",
        max_length=settings.MAX_LEN_EMAIL_USER_MODEL,
        blank=False,
        unique=True,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=settings.MAX_LEN_HASH_PASSWORD_USER_MODEL,
        blank=False,
    )
    is_active = models.BooleanField(
        "Активный",
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    @staticmethod
    def send_mail(self, mail):
        subject = mail["subject"]
        message = mail["message"]
        send_mail(
            subject=f"Confirmation of {subject}",
            message=f"Перейдите по ссылке, чтобы подтвердить действие: {message}",
            recipient_list=[
                self.email,
            ],
            from_email=settings.EMAIL_HOST_USER,
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
