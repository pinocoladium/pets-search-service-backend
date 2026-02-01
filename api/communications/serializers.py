from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.communications.models import Message, Notification


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            'id',
            'created_at',
            'recipient',
            'title',
            'text',
            'is_read',
        )


class MessageSerializer(ModelSerializer):
    sender = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault()),
        required=False,
    )

    class Meta:
        model = Message
        fields = (
            'id',
            'created_at',
            'recipient',
            'sender',
            'text',
            'is_read',
        )

        read_only_fields = (
            'created_at',
            'sender',
            'is_read',
        )
