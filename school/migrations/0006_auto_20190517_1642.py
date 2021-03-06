# Generated by Django 2.1.7 on 2019-05-17 08:42

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20190517_1642'),
        ('school', '0005_auto_20190517_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastoralstructure',
            name='kpi_pairs',
            field=models.ManyToManyField(blank=True, to='tracker.KPIPair'),
        ),
        migrations.AddField(
            model_name='pastoralstructure',
            name='kpis',
            field=models.ManyToManyField(blank=True, to='tracker.StandardisedData'),
        ),
        migrations.AddField(
            model_name='pastoralstructure',
            name='leaders',
            field=models.ManyToManyField(blank=True, to='school.Teacher'),
        ),
        migrations.AddField(
            model_name='pastoralstructure',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='school.PastoralStructure'),
        ),
        migrations.AddField(
            model_name='academicstructure',
            name='classgroups',
            field=models.ManyToManyField(blank=True, to='school.ClassGroup'),
        ),
        migrations.AddField(
            model_name='academicstructure',
            name='kpi_pairs',
            field=models.ManyToManyField(blank=True, to='tracker.KPIPair'),
        ),
        migrations.AddField(
            model_name='academicstructure',
            name='kpis',
            field=models.ManyToManyField(blank=True, to='tracker.StandardisedData'),
        ),
        migrations.AddField(
            model_name='academicstructure',
            name='leaders',
            field=models.ManyToManyField(blank=True, to='school.Teacher'),
        ),
        migrations.AddField(
            model_name='academicstructure',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='school.AcademicStructure'),
        ),
        migrations.AddField(
            model_name='classgroup',
            name='academic_position',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.AcademicStructure'),
        ),
        migrations.AddField(
            model_name='student',
            name='academic_tutorgroup',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.PastoralStructure'),
        ),
        migrations.AddField(
            model_name='tutorgroup',
            name='pastoral_link',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.PastoralStructure'),
        ),
    ]
