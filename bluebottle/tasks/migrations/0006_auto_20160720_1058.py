# Generated by Django 1.9.6 on 2016-07-20 08:58

from django.db import migrations


def set_task_type(apps, schema_editor):
    # Let's guess the taksk type.
    # If money_asked == 0 it's a sourcing project
    # and we asume 'event' task
    Task = apps.get_model("tasks", "Task")
    Task.objects.filter(project__amount_asked__gt=0).update(type='ongoing')
    Task.objects.filter(project__amount_asked=0).update(type='event')
    Task.objects.filter(project__amount_asked__isnull=True).update(type='event')

def reset_task_type(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Task = apps.get_model("tasks", "Task")
    Task.objects.update(type='ongoing')

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160706_1423'),
    ]

    operations = [
        migrations.RunPython(set_task_type, reset_task_type),
    ]
