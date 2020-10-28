# Generated by Django 1.10.8 on 2017-11-22 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0053_merge_20171122_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['title'], 'permissions': (('approve_payout', 'Can approve payouts for projects'), ('api_read_project', 'Can view projects through the API'), ('api_add_project', 'Can add projects through the API'), ('api_change_project', 'Can change projects through the API'), ('api_delete_project', 'Can delete projects through the API'), ('api_read_own_project', 'Can view own projects through the API'), ('api_add_own_project', 'Can add own projects through the API'), ('api_change_own_project', 'Can change own projects through the API'), ('api_change_own_running_project', 'Can change own running projects through the API'), ('api_delete_own_project', 'Can delete own projects through the API'), ('api_read_projectdocument', 'Can view project documents through the API'), ('api_add_projectdocument', 'Can add project documents through the API'), ('api_change_projectdocument', 'Can change project documents through the API'), ('api_delete_projectdocument', 'Can delete project documents through the API'), ('api_read_own_projectdocument', 'Can view project own documents through the API'), ('api_add_own_projectdocument', 'Can add own project documents through the API'), ('api_change_own_projectdocument', 'Can change own project documents through the API'), ('api_delete_own_projectdocument', 'Can delete own project documents through the API'), ('api_read_projectbudgetline', 'Can view project budget lines through the API'), ('api_add_projectbudgetline', 'Can add project budget lines through the API'), ('api_change_projectbudgetline', 'Can change project budget lines through the API'), ('api_delete_projectbudgetline', 'Can delete project budget lines through the API'), ('api_read_own_projectbudgetline', 'Can view own project budget lines through the API'), ('api_add_own_projectbudgetline', 'Can add own project budget lines through the API'), ('api_change_own_projectbudgetline', 'Can change own project budget lines through the API'), ('api_delete_own_projectbudgetline', 'Can delete own project budget lines through the API')), 'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
        migrations.AlterField(
            model_name='projectsearchfilter',
            name='name',
            field=models.CharField(choices=[(b'location', 'Location'), (b'theme', 'Theme'), (b'skills', 'Skill'), (b'date', 'Date'), (b'status', 'Status'), (b'type', 'Type'), (b'category', 'Category')], max_length=100),
        ),
    ]
