# Generated by Django 3.0.5 on 2021-04-26 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_auto_20210425_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 27, 1, 55, 11, 61517, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pay',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 27, 1, 55, 11, 61517, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='refund',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 27, 1, 55, 11, 62515, tzinfo=utc)),
        ),
    ]
