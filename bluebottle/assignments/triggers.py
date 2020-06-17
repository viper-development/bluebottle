from django.utils.translation import ugettext_lazy as _

from bluebottle.assignments.messages import AssignmentDateChanged
from bluebottle.assignments.models import Assignment, Applicant
from bluebottle.assignments.states import AssignmentStateMachine, ApplicantStateMachine
from bluebottle.fsm.effects import TransitionEffect, RelatedTransitionEffect
from bluebottle.fsm.triggers import ModelChangedTrigger, ModelDeletedTrigger
from bluebottle.notifications.effects import NotificationEffect


class DateChangedTrigger(ModelChangedTrigger):
    field = 'date'

    effects = [
        NotificationEffect(AssignmentDateChanged),
        TransitionEffect(
            'succeed',
            conditions=[
                AssignmentStateMachine.should_finish,
                AssignmentStateMachine.has_accepted_applicants
            ]
        ),
        TransitionEffect(
            'expire',
            conditions=[
                AssignmentStateMachine.should_finish,
                AssignmentStateMachine.has_no_accepted_applicants
            ]
        ),
        TransitionEffect(
            'reopen',
            conditions=[
                AssignmentStateMachine.should_open
            ]
        ),
        TransitionEffect(
            'lock',
            conditions=[
                AssignmentStateMachine.is_full
            ]
        ),
    ]


class RegistrationDeadlineChangedTrigger(ModelChangedTrigger):
    field = 'registration_deadline'

    effects = [
        NotificationEffect(AssignmentDateChanged),
        TransitionEffect(
            'start',
            conditions=[
                AssignmentStateMachine.should_start,
                AssignmentStateMachine.has_accepted_applicants
            ]
        ),
        TransitionEffect(
            'expire',
            conditions=[
                AssignmentStateMachine.should_start,
                AssignmentStateMachine.has_no_accepted_applicants
            ]
        ),
    ]


class CapacityChangedTrigger(ModelChangedTrigger):
    field = 'capacity'

    effects = [
        TransitionEffect('reopen', conditions=[AssignmentStateMachine.is_not_full]),
        TransitionEffect('lock', conditions=[AssignmentStateMachine.is_full]),
    ]


Assignment.triggers = [CapacityChangedTrigger, DateChangedTrigger, RegistrationDeadlineChangedTrigger]


class TimeSpentChangedTrigger(ModelChangedTrigger):
    field = 'time_spent'

    effects = [
        TransitionEffect('mark_present', conditions=[ApplicantStateMachine.has_time_spent]),
        TransitionEffect('mark_absent', conditions=[ApplicantStateMachine.has_no_time_spent]),
    ]


class ApplicantDeletedTrigger(ModelDeletedTrigger):
    title = _('delete this participant')
    effects = [
        RelatedTransitionEffect(
            'activity',
            'close',
            conditions=[
                ApplicantStateMachine.assignment_is_finished,
                ApplicantStateMachine.assignment_will_be_empty
            ]
        ),
        RelatedTransitionEffect(
            'activity',
            'reopen',
            conditions=[
                ApplicantStateMachine.assignment_will_become_open,
                ApplicantStateMachine.assignment_is_not_finished
            ],
        ),
    ]


Applicant.triggers = [TimeSpentChangedTrigger, ApplicantDeletedTrigger]
