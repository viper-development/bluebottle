# Generated by Django 1.10.8 on 2019-03-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_projects', '0014_merge_20180412_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectphase',
            options={'ordering': ['sequence'], 'permissions': (('api_read_projectphase', 'Can view project phase through API'),), 'verbose_name': 'project phase', 'verbose_name_plural': 'project phases'},
        ),
        migrations.AlterModelOptions(
            name='projecttheme',
            options={'ordering': ['translations__name'], 'permissions': (('api_read_projecttheme', 'Can view project theme through API'),), 'verbose_name': 'project theme', 'verbose_name_plural': 'project themes'},
        ),
        migrations.AlterField(
            model_name='projectphase',
            name='editable',
            field=models.BooleanField(default=True, help_text='Whether the project owner can change the details of the project.'),
        ),
        migrations.AlterUniqueTogether(
            name='projectphasetranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='projectthemetranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
