# Generated by Django 2.1.7 on 2019-03-18 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_auto_20190318_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpttrating',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 18, 10, 55, 26, 288458)),
        ),
    ]
