# Generated by Django 2.0.1 on 2018-02-07 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20180207_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='idnumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
