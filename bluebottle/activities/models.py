from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

from bluebottle.fsm import FSMField, TransitionManager, TransitionsMixin

from polymorphic.models import PolymorphicModel
from bluebottle.initiatives.models import Initiative
from bluebottle.activities.transitions import ActivityReviewTransitions
from bluebottle.activities.transitions import (
    ActivityTransitions, ContributionTransitions, OrganizerTransitions
)
from bluebottle.follow.models import Follow
from bluebottle.utils.models import ValidatedModelMixin, AnonymizationMixin
from bluebottle.utils.utils import get_current_host, get_current_language


class Activity(TransitionsMixin, AnonymizationMixin, ValidatedModelMixin, PolymorphicModel):
    owner = models.ForeignKey(
        'members.Member',
        verbose_name=_('owner'),
        related_name='activities',
    )

    highlight = models.BooleanField(default=False,
                                    help_text=_('Highlight this activity to show it on homepage'))

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    transition_date = models.DateTimeField(
        _('contribution date'),
        help_text=_('Date the contribution took place.'),
        null=True, blank=True
    )

    status = FSMField(
        default=ActivityTransitions.default
    )

    review_status = FSMField(
        default=ActivityReviewTransitions.default
    )

    initiative = models.ForeignKey(Initiative, related_name='activities')

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=100, default='new')
    description = models.TextField(
        _('description'), blank=True
    )

    followers = GenericRelation('follow.Follow', object_id_field='instance_id')
    messages = GenericRelation('notifications.Message')

    review_transitions = TransitionManager(ActivityReviewTransitions, 'review_status')
    follows = GenericRelation(Follow, object_id_field='instance_id')

    needs_review = False

    @property
    def stats(self):
        return {}

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        permissions = (
            ('api_read_activity', 'Can view activity through the API'),
            ('api_read_own_activity', 'Can view own activity through the API'),
        )

    def __unicode__(self):
        return self.title or str(_('-empty-'))

    def save(self, **kwargs):
        if self.slug in ['', 'new']:
            if self.title and slugify(self.title):
                self.slug = slugify(self.title)
            else:
                self.slug = 'new'

        if not self.owner_id:
            self.owner = self.initiative.owner

        super(Activity, self).save(**kwargs)
        Organizer.objects.update_or_create(
            activity=self,
            defaults={
                'user': self.owner
            }
        )

    def get_absolute_url(self):
        domain = get_current_host()
        language = get_current_language()
        link = u"{}/{}/initiatives/activities/details/{}/{}/{}".format(
            domain, language,
            self.__class__.__name__.lower(),
            self.pk,
            self.slug
        )
        return link


def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    # This fixing deleting related polymorphic objects through admin
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Contribution(TransitionsMixin, AnonymizationMixin, PolymorphicModel):
    status = FSMField(
        default=ContributionTransitions.values.new,
    )

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    transition_date = models.DateTimeField(null=True, blank=True)
    contribution_date = models.DateTimeField()

    activity = models.ForeignKey(Activity, related_name='contributions', on_delete=NON_POLYMORPHIC_CASCADE)
    user = models.ForeignKey('members.Member', verbose_name=_('user'), null=True, blank=True)

    @property
    def owner(self):
        return self.user

    @property
    def date(self):
        return self.activity.contribution_date

    def save(self, *args, **kwargs):
        if not self.contribution_date:
            self.contribution_date = self.date

        super(Contribution, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class Organizer(Contribution):
    transitions = TransitionManager(OrganizerTransitions, 'status')

    class Meta:
        verbose_name = _("Organizer")
        verbose_name_plural = _("Organizers")

    class JSONAPIMeta:
        resource_name = 'contributions/organizers'

    def save(self, *args, **kwargs):
        if not self.contribution_date:
            self.contribution_date = self.activity.created

        super(Organizer, self).save()


from bluebottle.activities.signals import *  # noqa
from bluebottle.activities.wallposts import *  # noqa
