# Generated by Django 5.0 on 2023-12-28 23:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0004_alter_subscription_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(null=True),
        ),
    ]
