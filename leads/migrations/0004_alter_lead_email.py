# Generated by Django 5.0 on 2024-01-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0003_alter_lead_mobile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="email",
            field=models.EmailField(max_length=150, unique=True, verbose_name="email"),
        ),
    ]
