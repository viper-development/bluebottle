# Generated by Django 1.10.2 on 2016-12-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_merge_20161213_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareresultscontent',
            name='share_text',
            field=models.CharField(default='', help_text=b'{amount}, {projects}, {tasks}, {hours}, {votes}, {people} will be replaced by live statistics', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stat',
            name='type',
            field=models.CharField(choices=[(b'manual', 'Manual input'), (b'people_involved', 'People involved'), (b'projects_realized', 'Projects realised'), (b'tasks_realized', 'Tasks realised'), (b'donated_total', 'Donated total'), (b'amount_matched', 'Amount matched'), (b'projects_online', 'Projects Online'), (b'votes_cast', 'Votes casts')], max_length=40),
        ),
    ]
