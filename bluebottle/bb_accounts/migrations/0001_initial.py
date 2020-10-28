# Generated by Django 1.9.4 on 2016-05-23 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(blank=True, max_length=100)),
                ('line2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=20)),
                ('address_type', models.CharField(blank=True, choices=[(b'primary', 'Primary'), (b'secondary', 'Secondary')], default=b'primary', max_length=10, verbose_name='address type')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.Country')),
            ],
            options={
                'db_table': 'members_useraddress',
                'verbose_name': 'user address',
                'verbose_name_plural': 'user addresses',
            },
        ),
    ]
