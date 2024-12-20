# Generated by Django 5.1.3 on 2024-11-27 06:58

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=255)),
                (
                    "password",
                    models.CharField(
                        max_length=255,
                        validators=[app.models.validate_password],
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("admin", "Admin"), ("user", "User")],
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
