# Generated by Django 1.11.15 on 2020-09-04 08:33

import bluebottle.files.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0011_auto_20200422_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='video',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=b'banner_slides/', validators=[bluebottle.files.validators.validate_video_file_size], verbose_name='video'),
        ),
    ]
