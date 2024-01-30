# Generated by Django 5.0 on 2024-01-30 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Academy_class", "0005_classattendance_walk_in_user_and_more"),
        ("subscriptions", "0016_subscription_refunded_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="walkinuser",
            name="academy_class",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="academy_class_walk_in_users",
                to="Academy_class.academyclass",
            ),
        ),
    ]
