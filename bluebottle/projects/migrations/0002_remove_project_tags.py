# Generated by Django 1.9.6 on 2016-05-31 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='tags',
        ),
    ]
