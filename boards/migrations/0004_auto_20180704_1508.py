# Generated by Django 2.0.6 on 2018-07-04 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20180704_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referral',
            old_name='board',
            new_name='board_member',
        ),
    ]
