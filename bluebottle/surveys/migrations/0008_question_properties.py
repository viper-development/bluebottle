# Generated by Django 1.9.6 on 2016-09-19 15:48

from django.db import migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0007_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='properties',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
    ]
