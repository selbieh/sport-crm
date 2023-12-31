# Generated by Django 5.0 on 2023-12-29 21:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0005_alter_subscription_end_date"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="freezingrequest",
            name="plan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="plan_freezing_requests",
                to="subscriptions.plan",
            ),
        ),
        migrations.AddField(
            model_name="freezingrequest",
            name="requested_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="requested_by_freezing_requests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="freezingrequest",
            name="end_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="freezingrequest",
            name="start_date",
            field=models.DateField(),
        ),
    ]
