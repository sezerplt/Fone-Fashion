# Generated by Django 4.2.6 on 2024-02-15 18:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polatFashionApp', '0016_alter_discount_discount_date_alter_orderdata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 15, 18, 26, 11, 726119, tzinfo=datetime.timezone.utc), verbose_name='Bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 15, 18, 26, 11, 726119, tzinfo=datetime.timezone.utc), verbose_name='Satış tarihi'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Promasyon'),
        ),
    ]
