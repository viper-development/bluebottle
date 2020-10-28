# Generated by Django 1.11.15 on 2019-09-18 14:32

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0030_auto_20190918_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlainPayoutAccount',
            fields=[
                ('payoutaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.PayoutAccount')),
                ('document', bluebottle.utils.fields.PrivateFileField(max_length=110, upload_to=b'private/funding/documents')),
                ('ip_address', models.GenericIPAddressField(blank=True, default=None, null=True, verbose_name='IP address')),
            ],
            options={
                'verbose_name': 'payout document',
                'verbose_name_plural': 'payout documents',
            },
            bases=('funding.payoutaccount',),
        ),
    ]
