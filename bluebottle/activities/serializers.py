from rest_framework_json_api.serializers import PolymorphicModelSerializer

from bluebottle.activities.models import Contribution, Activity
from bluebottle.events.serializers import EventSerializer, ParticipantSerializer
from bluebottle.funding.serializers import FundingSerializer, DonationSerializer
from bluebottle.assignments.serializers import AssignmentSerializer, AssignmentParticipantSerializer


class ActivitySerializer(PolymorphicModelSerializer):

    polymorphic_serializers = [
        EventSerializer,
        FundingSerializer,
        AssignmentSerializer
    ]

    class Meta:
        model = Activity

    class JSONAPIMeta:
        included_resources = [
            'owner',
            'initiative',
            'place'
        ]


class ContributionSerializer(PolymorphicModelSerializer):

    polymorphic_serializers = [
        ParticipantSerializer,
        AssignmentParticipantSerializer,
        DonationSerializer
    ]

    class Meta:
        model = Contribution
