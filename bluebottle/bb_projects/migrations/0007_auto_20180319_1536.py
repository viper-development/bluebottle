# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-19 14:36
from __future__ import unicode_literals

from django.core.exceptions import FieldError
from django.db import migrations, connection
from django.utils.translation import activate, _trans, ugettext as _

from tenant_extras.middleware import tenant_translation

from bluebottle.clients.utils import LocalTenant
from bluebottle.utils.utils import get_languages


def create_refunded_phase(apps, schema_editor):
    ProjectPhase = apps.get_model('bb_projects', 'ProjectPhase')
    try:
        ProjectPhase.objects.get_or_create(
            id=13, slug='refunded', viewable=True, editable=False,
            sequence=11, description='The project was refunded'
        )
    except FieldError:
        # If project phases are already translated then translate description
        object, created = ProjectPhase.objects.get_or_create(
            id=13, slug='refunded', viewable=True, editable=False,
            sequence=11
        )
        Client = apps.get_model('clients', 'Client')
        PhaseTranslation = apps.get_model('bb_projects', 'ProjectPhaseTranslation')

        tenant = Client.objects.get(schema_name=connection.tenant.schema_name)

        with LocalTenant(tenant):
            languages = get_languages()
            for (language, _long_language) in languages:
                activate(language)
                _trans._active.value = tenant_translation(language, tenant.client_name)
                PhaseTranslation.objects.create(
                    master_id=object.pk,
                    language_code=language,
                    name=_('Refunded'),
                    description=_('The project was refunded'),
                )


class Migration(migrations.Migration):

    dependencies = [
        ('bb_projects', '0006_add_group_permissions'),
    ]

    operations = [
    ]
