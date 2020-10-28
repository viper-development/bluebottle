# Generated by Django 1.11.15 on 2019-06-04 12:58

import bluebottle.fsm
import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('funding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', bluebottle.fsm.FSMField(default=b'new', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='funding',
            name='target',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='funding',
            name='target_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='payment',
            name='donation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='funding.Donation'),
        ),
        migrations.AddField(
            model_name='payment',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_funding.payment_set+', to='contenttypes.ContentType'),
        ),
    ]
