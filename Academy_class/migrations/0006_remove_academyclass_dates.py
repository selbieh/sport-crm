# Generated by Django 5.0 on 2024-02-04 20:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Academy_class", "0005_classattendance_walk_in_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="academyclass",
            name="dates",
        ),
    ]