# Generated by Django 2.1.2 on 2019-03-08 06:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20190308_1413'),
        ('tracker', '0002_auto_20190308_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardisedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_value', models.DecimalField(decimal_places=1, max_digits=5)),
                ('min_value', models.DecimalField(decimal_places=1, max_digits=5)),
                ('step', models.DecimalField(decimal_places=1, max_digits=5)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tracker.StandardisedData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardisedResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.DecimalField(decimal_places=1, max_digits=5)),
                ('standardised_data', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.StandardisedData')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
            ],
        ),
        migrations.AlterField(
            model_name='mpttrating',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 8, 14, 15, 13, 975196)),
        ),
    ]