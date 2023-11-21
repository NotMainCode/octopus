"""Custom model fields."""

from django.db import models

from users.validators import CustomEmailValidator


class CustomEmailField(models.EmailField):
    """Django EmailField with CustomEmailValidator."""

    default_validators = (CustomEmailValidator,)
