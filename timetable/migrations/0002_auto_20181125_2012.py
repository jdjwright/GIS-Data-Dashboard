# Generated by Django 2.0.1 on 2018-11-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsuspension',
            name='classgroups',
            field=models.ManyToManyField(blank=True, to='school.ClassGroup'),
        ),
    ]
