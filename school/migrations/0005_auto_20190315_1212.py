# Generated by Django 2.1.7 on 2019-03-15 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20190312_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicstructure',
            name='classgroups',
            field=models.ManyToManyField(blank=True, to='school.ClassGroup'),
        ),
        migrations.AddField(
            model_name='pastoralstructure',
            name='classgroups',
            field=models.ManyToManyField(blank=True, to='school.ClassGroup'),
        ),
        migrations.AddField(
            model_name='student',
            name='eal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='learning_support',
            field=models.CharField(blank=True, choices=[('S', 'S'), ('SA', 'SA'), ('M', 'M'), ('SS', 'SS'), ('N', 'N')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='academicstructure',
            name='kpis',
            field=models.ManyToManyField(blank=True, to='tracker.StandardisedData'),
        ),
        migrations.AlterField(
            model_name='academicstructure',
            name='leaders',
            field=models.ManyToManyField(blank=True, to='school.Teacher'),
        ),
        migrations.AlterField(
            model_name='pastoralstructure',
            name='kpis',
            field=models.ManyToManyField(blank=True, to='tracker.StandardisedData'),
        ),
        migrations.AlterField(
            model_name='pastoralstructure',
            name='leaders',
            field=models.ManyToManyField(blank=True, to='school.Teacher'),
        ),
    ]