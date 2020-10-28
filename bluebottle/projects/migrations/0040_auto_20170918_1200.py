# Generated by Django 1.10.8 on 2017-09-18 10:00

import bluebottle.utils.fields
from django.db import migrations, models
import django.utils.timezone
import django_summernote.settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0039_add_project_image_group_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectimage',
            options={'permissions': (('api_read_projectimage', 'Can view project imagesthrough the API'), ('api_add_projectimage', 'Can add project images through the API'), ('api_change_projectimage', 'Can change project images through the API'), ('api_delete_projectimage', 'Can delete project images through the API'), ('api_read_own_projectimage', 'Can view own project images through the API'), ('api_add_own_projectimage', 'Can add own project images through the API'), ('api_change_own_projectimage', 'Can change own project images through the API'), ('api_delete_own_projectimage', 'Can delete own project images through the API')), 'verbose_name': 'project image', 'verbose_name_plural': 'project images'},
        ),
        migrations.AddField(
            model_name='projectimage',
            name='file',
            field=models.FileField(default=None, upload_to=django_summernote.settings.uploaded_filepath),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectimage',
            name='name',
            field=models.CharField(blank=True, help_text=b'Defaults to filename, if left blank', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='projectimage',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='story',
            field=models.TextField(blank=True, help_text='Describe the project in detail', null=True, verbose_name='story'),
        ),
        migrations.AlterField(
            model_name='projectdocument',
            name='file',
            field=bluebottle.utils.fields.PrivateFileField(max_length=110, upload_to=b'private/private/private/projects/documents'),
        ),
    ]
