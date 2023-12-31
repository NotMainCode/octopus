"""Database settings of the 'Users' app."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from applications.users.fields import CustomEmailField
from applications.users.managers import CustomUserManager
from applications.users.validators import validate_first_name_and_last_name_fields


class User(AbstractUser):
    """User table settings."""

    username = None
    first_name = models.CharField(
        verbose_name="first name",
        max_length=settings.MAX_LEN_FULL_NAME_USER_MODEL,
        blank=False,
        validators=(
            validate_first_name_and_last_name_fields,
            MinLengthValidator(settings.MIN_LEN_FULL_NAME_USER_MODEL),
        ),
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=settings.MAX_LEN_FULL_NAME_USER_MODEL,
        blank=False,
        validators=(
            validate_first_name_and_last_name_fields,
            MinLengthValidator(settings.MIN_LEN_FULL_NAME_USER_MODEL),
        ),
    )
    email = CustomEmailField(
        verbose_name="email",
        max_length=settings.MAX_LEN_EMAIL_USER_MODEL,
        blank=False,
        unique=True,
    )
    password = models.CharField(
        verbose_name="password",
        max_length=settings.MAX_LEN_HASH_PASSWORD_USER_MODEL,
        blank=False,
    )
    is_active = models.BooleanField(
        "activity status",
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
