# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0012_auto_20200812_1024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='impactstatistictranslation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='impactstatistictranslation',
            name='master',
        ),
        migrations.AlterModelOptions(
            name='basestatistic',
            options={'ordering': ['sequence'], 'verbose_name': 'Statistic', 'verbose_name_plural': 'Statistics'},
        ),
        migrations.AlterModelOptions(
            name='databasestatistic',
            options={'verbose_name': 'Engagement statistic', 'verbose_name_plural': 'Engagement statistics'},
        ),
        migrations.AlterModelOptions(
            name='databasestatistictranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Engagement statistic Translation'},
        ),
        migrations.AlterModelOptions(
            name='impactstatistic',
            options={'verbose_name': 'Impact statistic', 'verbose_name_plural': 'Impact statistics'},
        ),
        migrations.AlterModelOptions(
            name='manualstatistic',
            options={'verbose_name': 'Custom statistic', 'verbose_name_plural': 'Custom statistics'},
        ),
        migrations.AlterModelOptions(
            name='manualstatistictranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Custom statistic Translation'},
        ),
        migrations.AlterModelManagers(
            name='impactstatistic',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='databasestatistic',
            name='query',
            field=models.CharField(choices=[(b'people_involved', 'People involved'), (b'participants', 'Participants'), (b'activities_succeeded', 'Activities succeeded'), (b'assignments_succeeded', 'Tasks succeeded'), (b'events_succeeded', 'Events succeeded'), (b'fundings_succeeded', 'Funding activities succeeded'), (b'assignment_members', 'Task applicants'), (b'event_members', 'Event participants'), (b'assignments_online', 'Tasks online'), (b'events_online', 'Events online'), (b'fundings_online', 'Funding activities online'), (b'donations', 'Donations'), (b'donated_total', 'Donated total'), (b'pledged_total', 'Pledged total'), (b'amount_matched', 'Amount matched'), (b'activities_online', 'Activities Online'), (b'time_spent', 'Time spent'), (b'members', 'Number of members')], db_index=True, max_length=30, verbose_name='query'),
        ),
        migrations.AlterField(
            model_name='manualstatistic',
            name='icon',
            field=models.CharField(blank=True, choices=[(b'people', 'People'), (b'time', 'Time'), (b'money', 'Money'), (b'trees', 'Trees'), (b'animals', 'Animals'), (b'jobs', 'Jobs'), (b'co2', 'C02'), (b'water', 'Water'), (b'plastic', 'plastic'), (b'task', 'Task'), (b'task-completed', 'Task completed'), (b'event', 'Event'), (b'event-completed', 'Event completed'), (b'funding', 'Funding'), (b'funding-completed', 'Funding completed')], max_length=20, null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='language',
            field=models.CharField(blank=True, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokm\xe5l'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], max_length=5, null=True, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='type',
            field=models.CharField(choices=[(b'manual', 'Manual'), (b'donated_total', 'Donated total'), (b'pledged_total', 'Pledged total'), (b'tasks_realized', 'Tasks realized'), (b'task_members', 'Taskmembers'), (b'people_involved', 'People involved'), (b'participants', 'Participants'), (b'amount_matched', 'Amount Matched'), (b'votes_cast', 'Number of votes cast'), (b'members', 'Number of members')], db_index=True, default=b'manual', max_length=20, verbose_name='Type'),
        ),
        migrations.DeleteModel(
            name='ImpactStatisticTranslation',
        ),
    ]