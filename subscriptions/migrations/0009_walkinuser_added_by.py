# Generated by Django 5.0 on 2024-01-04 23:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0008_walkintype_walkinuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="walkinuser",
            name="added_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="added_by_walk_in_users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]