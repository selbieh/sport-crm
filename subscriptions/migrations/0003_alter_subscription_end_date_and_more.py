# Generated by Django 5.0 on 2023-12-28 22:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "subscriptions",
            "0002_alter_plan_options_subscription_freezing_days_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="start_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
