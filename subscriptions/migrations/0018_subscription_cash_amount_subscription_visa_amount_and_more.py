# Generated by Django 5.0 on 2024-02-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0017_walkinuser_academy_class"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="cash_amount",
            field=models.DecimalField(
                decimal_places=3, max_digits=10, null=True, verbose_name="cash_amount"
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="visa_amount",
            field=models.DecimalField(
                decimal_places=3, max_digits=10, null=True, verbose_name="visa_amount"
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="start_date",
            field=models.DateField(null=True),
        ),
    ]
