# Generated by Django 2.1.7 on 2019-03-18 05:55

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_student_academic_tutorgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='academic_tutorgroup',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.PastoralStructure'),
        ),
    ]
