# Generated by Django 1.10.2 on 2016-12-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20161214_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supportertotalcontent',
            options={'verbose_name': 'Supporter total'},
        ),
        migrations.AddField(
            model_name='supportertotalcontent',
            name='co_financer_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
