# Generated by Django 2.1.7 on 2019-03-12 05:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20190311_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='paststandardisedresult',
            name='residual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standardisedresult',
            name='residual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mark',
            name='percent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mpttrating',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 12, 13, 0, 56, 923271)),
        ),
    ]
