# Generated by Django 1.10.2 on 2016-12-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_resultpage_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stat',
            options={'ordering': ['sequence']},
        ),
        migrations.AddField(
            model_name='stat',
            name='sequence',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
