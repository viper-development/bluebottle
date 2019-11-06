# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-23 10:36
from __future__ import unicode_literals

from datetime import timedelta

from django.db import migrations, connection, models
from django.utils.text import slugify
from django.contrib.gis.geos import Point


from bluebottle.clients import properties



def map_event_status(task):

    mapping = {
        'open': 'open',
        'full': 'full',
        'running': 'open',
        'realised': 'succeeded',
        'realized': 'succeeded',
        'in progress': 'open',
        'closed': 'closed'
    }
    status = mapping[task.status]
    if task.project.status in ['plan-new', 'draft', 'submitted']:
        status = 'draft'

    return status


def map_participant_status(member):
    mapping = {
        'applied': 'new',
        'accepted': 'new',
        'rejected': 'rejected',
        'stopped': 'closed',
        'withdrew': 'withdrawn',
        'realized': 'succeeded',
        'absent': 'no_show'
    }
    status = mapping[member.status]
    return status


def map_applicant_status(member):
    mapping = {
        'applied': 'new',
        'accepted': 'accepted',
        'rejected': 'rejected',
        'stopped': 'closed',
        'withdrew': 'withdrawn',
        'realized': 'succeeded',
        'absent': 'no_show'
    }
    status = mapping[member.status]
    return status


def migrate_tasks(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    properties.set_tenant(tenant)

    Task = apps.get_model('tasks', 'Task')

    Activity = apps.get_model('activities', 'Activity')
    Event = apps.get_model('events', 'Event')
    Assignment = apps.get_model('assignments', 'Assignment')

    Contribution = apps.get_model('activities', 'Contribution')
    Participant = apps.get_model('events', 'Participant')
    Applicant = apps.get_model('assignments', 'Applicant')

    Initiative = apps.get_model('initiatives', 'Initiative')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Wallpost = apps.get_model('wallposts', 'Wallpost')

    Place = apps.get_model('geo', 'Place')
    Geolocation = apps.get_model('geo', 'Geolocation')
    # Clean-up previous migrations of projects to initiatives
    Event.objects.all().delete()
    Assignment.objects.all().delete()

    event_ctype = ContentType.objects.get_for_model(Event)
    participant_ctype= ContentType.objects.get_for_model(Participant)
    assignment_ctype = ContentType.objects.get_for_model(Assignment)
    applicant_ctype= ContentType.objects.get_for_model(Applicant)
    task_ctype= ContentType.objects.get_for_model(Task)

    def get_location(task):
        place = Place.objects.filter(
            content_type=task_ctype,
            object_id=task.pk
        ).first()
        if place:
            return Geolocation.objects.create(
                street_number=place.street_number,
                street=place.street,
                postal_code=place.postal_code,
                locality=place.locality,
                province=place.province,
                position=Point(float(place.position.longitude), float(place.position.latitude)),
                country_id=place.country_id
            )
        else:
            return None

    for task in Task.objects.select_related('project').prefetch_related('members').iterator():
        if task.type == 'event' and (not task.skill_id or not task.skill.expertise):
            initiative = Initiative.objects.get(slug=task.project.slug)

            geolocation = get_location(task)
            status = map_event_status(task)

            event = Event.objects.create(
                # activity fields
                polymorphic_ctype=event_ctype,
                initiative=initiative,
                title=task.title,
                slug=slugify(task.title),
                description=task.description,
                review_status=initiative.status,
                status=status,
                owner_id=task.author_id,

                # event fields
                capacity=task.people_needed,
                automatically_accept=bool(task.accepting == 'automatic'),
                is_online=bool(not task.location),
                location=geolocation,
                location_hint=task.location,
                start_date=task.deadline.date(),
                start_time=task.deadline.time(),
                duration=task.time_needed,
                transition_date=task.deadline
            )
            task.activity_id = event.pk
            task.save()

            event.created = task.created
            event.updated = task.updated
            event.polymorphic_ctype = event_ctype
            event.save()

            for task_member in task.members.all():
                status = map_participant_status(task_member)

                participant = Participant.objects.create(
                    activity=event,
                    user=task_member.member,
                    status=status,
                    time_spent=task_member.time_spent,
                    transition_date=task.updated
                )
                participant.created = task.created
                participant.updated = task.updated
                participant.polymorphic_ctype = participant_ctype
                participant.save()

            old_ct = ContentType.objects.get_for_model(Task)
            Wallpost.objects.filter(content_type=old_ct, object_id=task.id).\
                update(content_type=event_ctype, object_id=event.id)

        else:
            initiative = Initiative.objects.get(slug=task.project.slug)
            geolocation = get_location(task)

            status = map_event_status(task)
            end_date_type = 'deadline'
            if task.type == 'event':
                end_date_type = 'on_date'

            assignment = Assignment.objects.create(
                # activity fields
                polymorphic_ctype=assignment_ctype,
                initiative=initiative,
                title=task.title,
                slug=slugify(task.title),
                description=task.description,
                status=status,
                review_status=initiative.status,
                owner=task.author,

                # assignment fields
                end_date_type=end_date_type,
                registration_deadline=task.deadline_to_apply.date(),
                end_date=task.deadline.date(),
                capacity=task.people_needed,
                is_online=bool(not task.location),
                location=geolocation,
                duration=task.time_needed,
                expertise=task.skill,
                transition_date=task.deadline
            )

            task.activity_id = assignment.pk
            task.save()

            assignment.created = task.created
            assignment.updated = task.updated
            assignment.polymorphic_ctype = assignment_ctype
            assignment.save()

            for task_member in task.members.all():
                status = map_applicant_status(task_member)

                applicant = Applicant.objects.create(
                    activity=assignment,
                    user=task_member.member,
                    status=status,
                    time_spent=task_member.time_spent,
                    motivation=task_member.motivation,
                    transition_date=task.updated
                )
                applicant.created = task.created
                applicant.updated = task.updated
                applicant.polymorphic_ctype = applicant_ctype
                applicant.save()

            old_ct = ContentType.objects.get_for_model(Task)
            Wallpost.objects.filter(content_type=old_ct, object_id=task.id). \
                update(content_type=assignment_ctype, object_id=assignment.id)


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0041_remove_untranslated_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='activity_id',
            field=models.IntegerField(null=True),
        ),
        migrations.RunPython(migrate_tasks, migrations.RunPython.noop)
    ]
