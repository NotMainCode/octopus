"""Database settings of the 'Companies' app."""

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    phones = models.TextField()  # Заглушка для модели Phones
    email = models.EmailField()
    address = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="companiues/logo/")
    website = models.URLField()
    fields = models.CharField(max_length=200)  # Заглушка для модели Fields
    industries = models.CharField(max_length=200)  # Заглушка для модели Industries
    team_size = models.PositiveIntegerField()
    year_founded = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
            MinLengthValidator(4),
            MaxLengthValidator(4),
        ],
    )

    def __str__(self):
        return self.name
