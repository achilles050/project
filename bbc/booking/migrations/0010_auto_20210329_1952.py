# Generated by Django 3.0.5 on 2021-03-29 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20210329_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherdetail',
            name='refund_percent',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
