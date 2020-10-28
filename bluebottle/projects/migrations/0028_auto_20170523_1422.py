# Generated by Django 1.10.7 on 2017-05-23 12:22
import os

from django.db import migrations, connection
from django.db.models import Value
from django.db.models.functions import Concat, Substr
from django.conf import settings
from django.utils._os import safe_join


def forward(apps, schema_editor):
    ProjectDocument = apps.get_model('projects', 'ProjectDocument')

    ProjectDocument.objects.exclude(file='').update(
        file=Concat(Value('private/'), 'file')
    )
    root = safe_join(
        settings.TENANT_BASE,
        connection.tenant.schema_name
    )

    old_dir = safe_join(root, 'projects/documents')
    new_dir = safe_join(root, 'private/projects/documents')

    if not os.path.exists(old_dir):
        return

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    os.rename(old_dir, new_dir)


def backward(apps, schema_editor):
    ProjectDocument = apps.get_model('projects', 'ProjectDocument')

    ProjectDocument.objects.filter(file__isnull=False).update(
        file=Substr('file', 9)
    )
    root = safe_join(
        settings.TENANT_BASE,
        connection.tenant.schema_name
    )

    old_dir = safe_join(root, 'private/projects/documents')
    new_dir = safe_join(root, 'projects/documents')

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    os.rename(old_dir, new_dir)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20170523_1422'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
