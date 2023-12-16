"""User manager model module."""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """UserManager for creating user and superuser without username field."""

    def create_user(self, email, password, **extra_fields):
        """Create user without username field."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create superuser without username field."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        """Normalize the email address by lowercase."""
        email = email or ""
        return email.lower()

    def _create_user(self, email, password, **extra_fields):
        """Create and save user without username field."""
        normalize_email = self.normalize_email(email)
        user = self.model(email=normalize_email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
