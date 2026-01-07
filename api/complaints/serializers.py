from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.complaints.models import Complaint


class ComplaintSerializer(ModelSerializer):
    creator = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault()),
        required=False,
    )

    class Meta:
        model = Complaint
        fields = (
            'id',
            'status',
            'creator',
            'object_type',
            'object_id',
            'text',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'creator',
            'created_at',
            'updated_at',
        )
