# Generated by Django 1.9.6 on 2016-09-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0012_auto_20160920_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggregateanswer',
            name='value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='link',
            field=models.URLField(null=True),
        ),
    ]
