# Generated by Django 4.2.6 on 2024-01-28 15:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polatFashionApp', '0007_alter_discount_discount_date_alter_orderdata_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Promasyon'),
        ),
        migrations.AddField(
            model_name='useddiscount',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userstatistics',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 28, 15, 11, 29, 389736, tzinfo=datetime.timezone.utc), verbose_name='Bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 28, 15, 11, 29, 389736, tzinfo=datetime.timezone.utc), verbose_name='Satış tarihi'),
        ),
    ]
