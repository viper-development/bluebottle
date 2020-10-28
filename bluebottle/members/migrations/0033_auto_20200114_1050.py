# Generated by Django 1.11.15 on 2020-01-14 09:50

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0032_auto_20191223_1456'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useractivity',
            options={'ordering': ['-created'], 'verbose_name': 'User activity', 'verbose_name_plural': 'User activities'},
        ),
        migrations.AddField(
            model_name='memberplatformsettings',
            name='closed',
            field=models.BooleanField(default=False, help_text='Require login before accessing the platform'),
        ),
        migrations.AddField(
            model_name='memberplatformsettings',
            name='confirm_signup',
            field=models.BooleanField(default=False, help_text="Require verifying the user's email before signup"),
        ),
        migrations.AddField(
            model_name='memberplatformsettings',
            name='email_domain',
            field=models.CharField(blank=True, help_text='Domain that all email should belong to', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='memberplatformsettings',
            name='login_methods',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('password', 'Email/password combination'), ('SSO', 'Company SSO')], default=['password'], max_length=100),
        ),
        migrations.AlterField(
            model_name='member',
            name='partner_organization',
            field=models.ForeignKey(blank=True, help_text='Users that are connected to a partner organisation will skip the organisation step in initiative create.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_organization_members', to='organizations.Organization', verbose_name='Partner organisation'),
        ),
    ]
