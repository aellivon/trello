# Generated by Django 2.0.6 on 2018-07-11 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_auto_20180711_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]