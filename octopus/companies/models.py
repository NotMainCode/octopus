"""Database settings of the 'Companies' app."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Industry(models.Model):
    """Industry table settings."""

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "industry"
        verbose_name_plural = "industries"

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    """ServiceCategory table settings."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "service category"
        verbose_name_plural = "service categories"


class Service(models.Model):
    """Service table settings."""

    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self):
        return self.name


class City(models.Model):
    """City table settings."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Company(models.Model):
    """Company table settings."""

    name = models.CharField("name", max_length=100)
    description = models.TextField("description")
    email = models.EmailField("email")
    address = models.CharField("address", max_length=200)
    logo = models.ImageField("logo", upload_to="companies/logo/")
    website = models.URLField("website")
    services = models.ManyToManyField(
        Service,
        related_name="companies",
        verbose_name="services",
    )
    industries = models.ManyToManyField(
        Industry,
        related_name="companies",
        verbose_name="industries",
    )
    team_size = models.PositiveIntegerField("team size")
    year_founded = models.PositiveIntegerField(
        "year founded",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ],
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="city",
        related_name="companies",
    )

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Favorite table settings."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="favorite",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="company",
        related_name="in_favorite",
    )

    class Meta:
        verbose_name = "favorite"
        verbose_name_plural = "favorite"
        ordering = ("company",)
        constraints = [
            models.UniqueConstraint(fields=["user", "company"], name="unique_favorite")
        ]

    def __str__(self):
        return f"{self.company} {self.user}"


class Phone(models.Model):
    """Phone table settings."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="phones",
        verbose_name="company",
    )
    number = models.CharField("number", max_length=18)

    def __str__(self):
        return self.number
