"""Database settings of the 'Users' app."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from applications.users.fields import CustomEmailField
from applications.users.managers import CustomUserManager
from applications.users.validators import validate_first_name_and_last_name_fields
from core.users.constants.field_limits import FIELD_LIMITS_USERS_APP


class User(AbstractUser):
    """User table settings."""

    username = None
    first_name = models.CharField(
        verbose_name="first name",
        max_length=FIELD_LIMITS_USERS_APP["user_full_name_max_char"],
        blank=False,
        validators=(
            validate_first_name_and_last_name_fields,
            MinLengthValidator(FIELD_LIMITS_USERS_APP["user_full_name_min_char"]),
        ),
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=FIELD_LIMITS_USERS_APP["user_full_name_max_char"],
        blank=False,
        validators=(
            validate_first_name_and_last_name_fields,
            MinLengthValidator(FIELD_LIMITS_USERS_APP["user_full_name_min_char"]),
        ),
    )
    email = CustomEmailField(
        verbose_name="email",
        max_length=FIELD_LIMITS_USERS_APP["email_max_char"],
        blank=False,
        unique=True,
    )
    password = models.CharField(
        verbose_name="password",
        max_length=FIELD_LIMITS_USERS_APP["password_hash_max_char"],
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
