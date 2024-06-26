# Generated by Django 4.2.6 on 2024-02-11 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polatFashionApp', '0015_promotion_state_alter_discount_discount_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 11, 14, 23, 3, 482476, tzinfo=datetime.timezone.utc), verbose_name='Bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 11, 14, 23, 3, 482476, tzinfo=datetime.timezone.utc), verbose_name='Satış tarihi'),
        ),
    ]
