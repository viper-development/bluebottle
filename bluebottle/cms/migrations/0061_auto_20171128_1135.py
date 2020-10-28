# Generated by Django 1.10.8 on 2017-11-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0060_merge_20171121_1334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentlink',
            options={'ordering': ['sequence']},
        ),
        migrations.AlterModelOptions(
            name='logo',
            options={'ordering': ['sequence']},
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'ordering': ['sequence']},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['sequence']},
        ),
        migrations.AlterField(
            model_name='categoriescontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='linkscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='locationscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='logoscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='projectimagescontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='projectscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='projectsmapcontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='quotescontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shareresultscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='slidescontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='statscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stepscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='supportertotalcontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='surveycontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taskscontent',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
