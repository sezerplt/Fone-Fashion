# Generated by Django 4.2.6 on 2024-02-10 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polatFashionApp', '0013_customuser_tel_alter_discount_discount_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='category',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='totalProduct',
        ),
        migrations.AddField(
            model_name='promotion',
            name='explanation',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='İndirim açıklaması'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 10, 10, 16, 12, 810363, tzinfo=datetime.timezone.utc), verbose_name='Bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 10, 10, 16, 12, 810363, tzinfo=datetime.timezone.utc), verbose_name='Satış tarihi'),
        ),
    ]
