"""Custom fields of the Users app models."""

from django.db import models

from applications.users.validators import CustomEmailValidator


class CustomEmailField(models.EmailField):
    """Django EmailField with CustomEmailValidator."""

    default_validators = (CustomEmailValidator(),)
