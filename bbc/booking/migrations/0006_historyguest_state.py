# Generated by Django 3.0.5 on 2021-03-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20210314_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyguest',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]
