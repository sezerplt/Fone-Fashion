# Generated by Django 4.2.6 on 2024-01-24 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polatFashionApp', '0003_alter_discount_discount_date_alter_orderdata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 24, 8, 10, 12, 31359, tzinfo=datetime.timezone.utc), verbose_name='Bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 24, 8, 10, 12, 32361, tzinfo=datetime.timezone.utc), verbose_name='Satış tarihi'),
        ),
    ]