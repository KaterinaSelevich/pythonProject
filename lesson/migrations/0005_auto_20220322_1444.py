# Generated by Django 3.0 on 2022-03-22 11:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0004_auto_20220320_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 11, 44, 47, 800164, tzinfo=utc)),
        ),
    ]
