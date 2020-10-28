# Generated by Django 1.9.6 on 2016-09-20 08:19

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20160829_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskMemberStatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, verbose_name='status')),
                ('start', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, help_text='When this task member entered in this status.', verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, verbose_name='status')),
                ('start', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, help_text='When this task entered in this status.', verbose_name='created')),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(b'open', 'Open'), (b'in progress', 'Running'), (b'realized', 'Realised'), (b'closed', 'Closed')], default=b'open', max_length=20, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='taskmember',
            name='status',
            field=models.CharField(choices=[(b'applied', 'Applied'), (b'accepted', 'Accepted'), (b'rejected', 'Rejected'), (b'stopped', 'Withdrew'), (b'realized', 'Realised')], default=b'applied', max_length=20, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='taskstatuslog',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='taskmemberstatuslog',
            name='task_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.TaskMember'),
        ),
    ]
