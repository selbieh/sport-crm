# Generated by Django 5.0 on 2023-12-28 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Package",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created_at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="modified_at"),
                ),
                (
                    "is_safe_deleted",
                    models.BooleanField(default=False, verbose_name="is_safe_delete"),
                ),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Package",
                "verbose_name_plural": "Packages",
            },
        ),
        migrations.CreateModel(
            name="Plan",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created_at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="modified_at"),
                ),
                (
                    "is_safe_deleted",
                    models.BooleanField(default=False, verbose_name="is_safe_delete"),
                ),
                ("name", models.CharField(max_length=150)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "duration_type",
                    models.CharField(
                        choices=[("Days", "Days"), ("Sessions", "Session")],
                        default="Days",
                        max_length=50,
                    ),
                ),
                ("number_of_days", models.IntegerField(null=True)),
                ("number_of_sessions", models.IntegerField(null=True)),
                ("number_of_duration_days", models.IntegerField()),
                ("number_of_freezing_days", models.IntegerField(default=0)),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="plans",
                        to="subscriptions.package",
                    ),
                ),
            ],
            options={
                "verbose_name": "Plan",
                "verbose_name_plural": "Planes",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created_at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="modified_at"),
                ),
                (
                    "is_safe_deleted",
                    models.BooleanField(default=False, verbose_name="is_safe_delete"),
                ),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("end_date", models.DateTimeField(auto_now_add=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="subscriptions",
                        to="subscriptions.plan",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="subscriptions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
            },
        ),
    ]
