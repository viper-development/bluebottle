# Generated by Django 1.10.8 on 2018-01-21 18:52

import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0064_auto_20180119_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcreatetemplate',
            name='default_pitch',
            field=models.TextField(blank=True, help_text='Default project pitch', null=True),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='default_amount_asked',
            field=bluebottle.utils.fields.MoneyField(blank=True, currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=None, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='default_image',
            field=models.ImageField(blank=True, help_text='Default project image', null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
