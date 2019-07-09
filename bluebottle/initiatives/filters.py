from bluebottle.utils.filters import ElasticSearchFilter
from bluebottle.initiatives.documents import InitiativeDocument


class InitiativeSearchFilter(ElasticSearchFilter):
    document = InitiativeDocument

    sort_fields = {
        'date': ('-created', ),
        'alphabetical': ('title_keyword', ),
    }

    filters = ('owner.id', 'theme.id', 'place.country', 'categories.id', 'categories.slug', )

    search_fields = (
        'status', 'title', 'story', 'pitch', 'place.locality', 'place.postal_code',
        'theme.name', 'owner.name', 'promoter.name',
    )

    boost = {'title': 2}
