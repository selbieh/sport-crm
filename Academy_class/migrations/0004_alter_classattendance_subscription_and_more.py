# Generated by Django 5.0 on 2024-01-10 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Academy_class", "0003_alter_academyclass_age_group_and_more"),
        ("subscriptions", "0013_subscription_discount_walkinuser_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classattendance",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="class_subscription_attendances",
                to="subscriptions.subscription",
            ),
        ),
        migrations.RemoveField(
            model_name="classattendance",
            name="is_attended",
        ),
        migrations.AddField(
            model_name="classattendance",
            name="academy_class",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="academy_class_attendance",
                to="Academy_class.academyclass",
            ),
        ),
        migrations.AddField(
            model_name="classattendance",
            name="checkin_time",
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name="classattendance",
            name="checkout_time",
            field=models.TimeField(null=True),
        ),
        migrations.DeleteModel(
            name="ClassSubscription",
        ),
    ]
