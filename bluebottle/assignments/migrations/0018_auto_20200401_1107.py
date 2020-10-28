# Generated by Django 1.11.15 on 2020-04-01 09:07

from django.db import migrations

def migrate_documents(apps, schema_editor):
    Applicant = apps.get_model('assignments', 'Applicant')
    PrivateDocument = apps.get_model('files', 'PrivateDocument')

    for applicant in Applicant.objects.all():
        if applicant.document:
            private = PrivateDocument.objects.create(
                owner=applicant.document.owner,
                created=applicant.document.created,
                file=applicant.document.file
            )
            applicant.private_document = private
            applicant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0017_applicant_private_document'),
    ]

    operations = [
        migrations.RunPython(migrate_documents, migrations.RunPython.noop)
    ]
