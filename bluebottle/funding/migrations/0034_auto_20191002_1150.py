# Generated by Django 1.11.15 on 2019-10-02 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0033_auto_20191002_0903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plainpayoutaccount',
            options={'verbose_name': 'plain payout account', 'verbose_name_plural': 'plain payout accounts'},
        ),
        migrations.RemoveField(
            model_name='bankaccount',
            name='owner',
        ),
    ]
