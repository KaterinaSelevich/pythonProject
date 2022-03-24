# Generated by Django 3.0 on 2022-03-22 15:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0007_auto_20220322_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='cover',
            field=models.ImageField(default='', upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 15, 46, 43, 894435, tzinfo=utc)),
        ),
    ]
