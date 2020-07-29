from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatedFields

from bluebottle.utils.models import SortableTranslatableModel

ICONS = [
    ('people', _('People')),
    ('time', _('Time')),
    ('money', _('Money')),
    ('trees', _('Trees')),
    ('animals', _('Animals')),
    ('jobs', _('Jobs')),
    ('co2', _('C02')),
    ('water', _('Water')),
    ('plastic', _('plastic')),
]


class ImpactType(SortableTranslatableModel):
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    active = models.BooleanField(_('active'), default=True)

    icon = models.CharField(
        _('icon'),
        choices=ICONS,
        null=True,
        blank=True,
        max_length=20
        help_text=_('Select the symbol that best represents your impact type.')
    )

    translations = TranslatedFields(
        name=models.CharField(
            _('Name'),
            max_length=100
        ),
        unit=models.CharField(
            _('unit'),
            blank=True,
            null=True,
            max_length=100,
            help_text=_('E.g. "liters" or "kg". Leave empty if irrelevant.')

        ),
        text=models.CharField(
            _('Title'),
            max_length=100,
            help_text=_('E.g. "save animals" or "reduce co2 emissions". '
                        'The title is displayed when the activity manager has to choose from the list of impact types.')
        ),
        text_with_target=models.CharField(
            _('Text including target'),
            max_length=100,
            help_text=_('Enter the same text as in the Title field and add "{}" where the value and unit should be placed. '
                        'E.g. "save {} animals" or "reduce co2 emissions by {}".')
        ),
        text_passed=models.CharField(
            _('Title in passed tense'),
            max_length=100,
            help_text=_('E.g. "animals saved" or "co2 emissions reduced".')
        ),
        text_passed_with_value=models.CharField(
            _('Text in passed tense with realized  value'),
            max_length=100,
            help_text=_('E.g. "{} animals saved" or "{} co2 emissions reduced".')
        ),
    )

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(ImpactType, self).save(**kwargs)

    class Meta:
        ordering = ['translations__name']
        verbose_name = _('impact type')
        verbose_name_plural = _('impact types')


class ImpactGoal(models.Model):
    type = models.ForeignKey(
        ImpactType,
        verbose_name=_('type'),
        related_name='goals'
    )
    activity = models.ForeignKey(
        'activities.activity',
        verbose_name=_('activity'),
        related_name='goals'
    )

    target = models.FloatField(_('Impact target'), blank=False, null=True)
    realized = models.FloatField(_('Impact result'), blank=False, null=True)
