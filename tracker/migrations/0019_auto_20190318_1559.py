# Generated by Django 2.1.7 on 2019-03-18 07:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0018_auto_20190318_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpttrating',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]