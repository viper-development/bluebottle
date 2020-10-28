# Generated by Django 1.10.8 on 2017-10-31 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsAdapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default=b'GoogleAnalytics', max_length=100)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnalyticsPlatformSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='analyticsadapter',
            name='analytics_settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adapters', to='analytics.AnalyticsPlatformSettings'),
        ),
    ]
