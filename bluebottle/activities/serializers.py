from rest_framework_json_api.relations import PolymorphicResourceRelatedField
from rest_framework_json_api.serializers import PolymorphicModelSerializer

from bluebottle.activities.models import Contribution, Activity
from bluebottle.assignments.serializers import ApplicantSerializer, AssignmentListSerializer
from bluebottle.events.serializers import ParticipantSerializer, EventListSerializer
from bluebottle.funding.serializers import DonationSerializer, FundingListSerializer
from bluebottle.transitions.serializers import TransitionSerializer


class ActivitySerializer(PolymorphicModelSerializer):

    polymorphic_serializers = [
        EventListSerializer,
        FundingListSerializer,
        AssignmentListSerializer
    ]

    included_serializers = {
        'owner': 'bluebottle.initiatives.serializers.MemberSerializer',
        'initiative': 'bluebottle.initiatives.serializers.InitiativeSerializer',
        'location': 'bluebottle.geo.serializers.GeolocationSerializer',
        'initiative.image': 'bluebottle.initiatives.serializers.InitiativeImageSerializer',
        'initiative.location': 'bluebottle.geo.serializers.LocationSerializer',
        'initiative.place': 'bluebottle.geo.serializers.GeolocationSerializer',
    }

    class Meta:
        model = Activity

        meta_fields = ('permissions', 'transitions', 'review_transitions', 'created', 'updated', 'errors', 'required', )

    class JSONAPIMeta:
        included_resources = [
            'owner',
            'initiative',
            'location',
            'initiative.image',
            'initiative.place',
            'initiative.location',
        ]


class ContributionSerializer(PolymorphicModelSerializer):

    polymorphic_serializers = [
        ParticipantSerializer,
        ApplicantSerializer,
        DonationSerializer
    ]

    class Meta:
        model = Contribution


class ActivityReviewTransitionSerializer(TransitionSerializer):
    resource = PolymorphicResourceRelatedField(ActivitySerializer, queryset=Activity.objects.all())
    field = 'review_transitions'
    included_serializers = {
        'resource': 'bluebottle.activities.serializers.ActivitySerializer',
    }

    class JSONAPIMeta:
        included_resources = ['resource']
        resource_name = 'activities/review-transitions'
