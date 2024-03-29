# Generated by Django 5.0 on 2024-01-30 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0015_alter_plan_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="refunded_amount",
            field=models.DecimalField(
                decimal_places=3,
                max_digits=10,
                null=True,
                verbose_name="refunded_amount",
            ),
        ),
        migrations.AlterField(
            model_name="walkinuser",
            name="walk_in_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="walk_in_users",
                to="subscriptions.walkintype",
            ),
        ),
    ]
