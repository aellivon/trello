# Generated by Django 2.0.6 on 2018-07-12 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_boardmember_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardcomment',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
