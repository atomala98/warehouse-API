# Generated by Django 3.1.7 on 2021-02-24 16:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 16, 52, 56, 601711, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(default=orders.models.order_number),
        ),
    ]