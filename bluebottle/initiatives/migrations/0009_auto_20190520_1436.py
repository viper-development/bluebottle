# Generated by Django 1.11.15 on 2019-05-20 12:36

import bluebottle.files.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0008_auto_20190513_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitiativePlatformSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True)),
                ('activity_types', multiselectfield.db.fields.MultiSelectField(choices=[(b'funding', 'Funding'), (b'event', 'Events'), (b'job', 'Jobs')], max_length=100)),
                ('require_organization', models.BooleanField(default=False)),
                ('share_options', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(b'twitter', 'Twitter'), (b'facebook', 'Facebook'), (b'facebookAtWork', 'Facebook at Work'), (b'linkedin', 'LinkedIn'), (b'whatsapp', 'Whatsapp'), (b'email', 'Email')], max_length=100)),
                ('facebook_at_work_url', models.URLField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'initiative platform settings',
                'verbose_name_plural': 'initiative platform settings',
            },
        ),
        migrations.AlterField(
            model_name='initiative',
            name='image',
            field=bluebottle.files.fields.ImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.Image'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_initiatives', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='promoter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='promoter'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_initiatives', to=settings.AUTH_USER_MODEL, verbose_name='reviewer'),
        ),
    ]
