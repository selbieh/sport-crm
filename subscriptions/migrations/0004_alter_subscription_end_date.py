# Generated by Django 5.0 on 2023-12-28 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0003_alter_subscription_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(),
        ),
    ]
