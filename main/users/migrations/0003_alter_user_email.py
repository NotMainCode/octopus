# Generated by Django 4.1 on 2023-11-21 21:45

from django.db import migrations
import users.model_fields


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=users.model_fields.CustomEmailField(
                max_length=254, unique=True, verbose_name="Почта"
            ),
        ),
    ]
