from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api.relations import ResourceRelatedField

from bluebottle.activities.utils import (
    BaseActivitySerializer, BaseContributionSerializer,
    BaseActivityListSerializer, BaseTinyActivitySerializer
)
from bluebottle.tasks.models import Skill
from bluebottle.assignments.filters import ApplicantListFilter
from bluebottle.assignments.models import Assignment, Applicant
from bluebottle.assignments.permissions import ApplicantDocumentPermission
from bluebottle.files.serializers import PrivateDocumentSerializer, PrivateDocumentField
from bluebottle.fsm.serializers import TransitionSerializer
from bluebottle.utils.serializers import ResourcePermissionField, FilteredRelatedField


class ApplicantDocumentSerializer(PrivateDocumentSerializer):
    content_view_name = 'applicant-document'
    relationship = 'applicant_set'


class AssignmentListSerializer(BaseActivityListSerializer):
    permissions = ResourcePermissionField('assignment-detail', view_args=('pk',))

    class Meta(BaseActivityListSerializer.Meta):
        model = Assignment
        fields = BaseActivityListSerializer.Meta.fields + (
            'is_online',
            'date',
            'local_date',
            'end_date_type',
            'registration_deadline',
            'capacity',
            'expertise',
            'duration',
            'location',
            'permissions',
            'preparation',
        )

    class JSONAPIMeta(BaseActivityListSerializer.JSONAPIMeta):
        resource_name = 'activities/assignments'
        included_resources = [
            'location',
            'expertise',
        ]

    included_serializers = dict(
        BaseActivityListSerializer.included_serializers,
        **{
            'expertise': 'bluebottle.assignments.serializers.SkillSerializer',
            'location': 'bluebottle.geo.serializers.GeolocationSerializer',
        }
    )


class TinyAssignmentSerializer(BaseTinyActivitySerializer):

    class Meta(BaseTinyActivitySerializer.Meta):
        model = Assignment
        fields = BaseTinyActivitySerializer.Meta.fields + ('end_date_type', 'date')

    class JSONAPIMeta(BaseTinyActivitySerializer.JSONAPIMeta):
        resource_name = 'activities/assignments'


class AssignmentSerializer(BaseActivitySerializer):
    permissions = ResourcePermissionField('assignment-detail', view_args=('pk',))
    contributions = FilteredRelatedField(many=True, filter_backend=ApplicantListFilter)

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if (
            not user.is_authenticated or (
                self.instance and (
                    user not in [
                        self.instance.owner,
                        self.instance.initiative.owner,
                        self.instance.initiative.activity_manager
                    ] and
                    not len(self.instance.applicants.filter(user=user))
                )
            )
        ):
            del fields['online_meeting_url']

        return fields

    class Meta(BaseActivitySerializer.Meta):
        model = Assignment
        fields = BaseActivitySerializer.Meta.fields + (
            'is_online',
            'online_meeting_url',
            'date',
            'local_date',
            'end_date_type',
            'registration_deadline',
            'capacity',
            'expertise',
            'duration',
            'location',
            'permissions',
            'contributions',
            'start_time',
            'preparation',
        )

    class JSONAPIMeta(BaseActivitySerializer.JSONAPIMeta):
        resource_name = 'activities/assignments'
        included_resources = BaseActivitySerializer.JSONAPIMeta.included_resources + [
            'location',
            'expertise',
            'contributions',
            'contributions.user',
            'contributions.document'
        ]

    included_serializers = dict(
        BaseActivitySerializer.included_serializers,
        **{
            'expertise': 'bluebottle.assignments.serializers.SkillSerializer',
            'location': 'bluebottle.geo.serializers.GeolocationSerializer',
            'contributions': 'bluebottle.assignments.serializers.ApplicantSerializer',
        }
    )


class AssignmentTransitionSerializer(TransitionSerializer):
    resource = ResourceRelatedField(queryset=Assignment.objects.all())
    field = 'states'
    included_serializers = {
        'resource': 'bluebottle.assignments.serializers.AssignmentSerializer',
    }

    class JSONAPIMeta:
        included_resources = ['resource', ]
        resource_name = 'assignment-transitions'


class ApplicantListSerializer(BaseContributionSerializer):
    time_spent = serializers.FloatField(required=False, allow_null=True)

    class Meta(BaseContributionSerializer.Meta):
        model = Applicant
        fields = BaseContributionSerializer.Meta.fields + (
            'time_spent',
        )

    class JSONAPIMeta(BaseContributionSerializer.JSONAPIMeta):
        resource_name = 'contributions/applicants'
        included_resources = [
            'user',
            'activity',
        ]

    included_serializers = {
        'activity': 'bluebottle.assignments.serializers.TinyAssignmentSerializer',
        'user': 'bluebottle.initiatives.serializers.MemberSerializer',
    }


class ApplicantSerializer(BaseContributionSerializer):
    time_spent = serializers.FloatField(required=False, allow_null=True)
    motivation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    document = PrivateDocumentField(required=False, allow_null=True, permissions=[ApplicantDocumentPermission])

    class Meta(BaseContributionSerializer.Meta):
        model = Applicant
        fields = BaseContributionSerializer.Meta.fields + (
            'time_spent',
            'motivation',
            'document'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Applicant.objects.all(),
                fields=('activity', 'user')
            )
        ]

    class JSONAPIMeta(BaseContributionSerializer.JSONAPIMeta):
        resource_name = 'contributions/applicants'
        included_resources = [
            'user',
            'activity',
            'document'
        ]

    included_serializers = {
        'activity': 'bluebottle.assignments.serializers.AssignmentListSerializer',
        'user': 'bluebottle.initiatives.serializers.MemberSerializer',
        'document': 'bluebottle.assignments.serializers.ApplicantDocumentSerializer',
    }


class ApplicantTransitionSerializer(TransitionSerializer):
    resource = ResourceRelatedField(queryset=Applicant.objects.all())
    field = 'states'
    included_serializers = {
        'resource': 'bluebottle.assignments.serializers.ApplicantSerializer',
        'resource.activity': 'bluebottle.assignments.serializers.AssignmentSerializer',
    }

    class JSONAPIMeta:
        resource_name = 'contributions/applicant-transitions'
        included_resources = [
            'resource',
            'resource.activity',
        ]


class SkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Skill
        fields = ('id', 'name', 'expertise')

    class JSONAPIMeta:
        included_resources = ['resource', ]
        resource_name = 'skills'
