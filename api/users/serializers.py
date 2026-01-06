from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserLocation


User = get_user_model()


class UserSerializer(ModelSerializer):
    password = serializers.CharField(
        label='Пароль',
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'is_admin',
            'name',
            'username',
            'email',
            'phone_number',
            'notifications_enabled',
            'password',
        )

        read_only_fields = ('is_admin',)


class UserLocationSerializer(ModelSerializer):
    class Meta:
        model = UserLocation
        fields = (
            'id',
            'title',
            'location',
        )
