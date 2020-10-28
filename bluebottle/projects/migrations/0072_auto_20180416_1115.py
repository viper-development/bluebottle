# Generated by Django 1.10.8 on 2018-04-16 09:15

import bluebottle.utils.fields
from django.db import migrations, models
import multiselectfield


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0071_merge_20180412_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectplatformsettings',
            name='facebook_at_work_url',
            field=models.URLField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='projectplatformsettings',
            name='share_options',
            field=multiselectfield.MultiSelectField(choices=[(b'twitter', 'Twitter'), (b'facebook', 'Facebook'), (b'facebookAtWork', 'Facebook at Work'), (b'linkedin', 'LinkedIn'), (b'whatsapp', 'Whatsapp'), (b'email', 'Email')], default=[], max_length=100),
            preserve_default=False,
        ),
    ]
