# Generated by Django 4.1 on 2023-11-18 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("companies", "0003_alter_favoriteslist_company_alter_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoritesList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_favorite",
                        to="companies.company",
                        verbose_name="Компания",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
                "ordering": ("company",),
            },
        ),
        migrations.AddConstraint(
            model_name="favoriteslist",
            constraint=models.UniqueConstraint(
                fields=("user", "company"), name="unique_favorite"
            ),
        ),
    ]