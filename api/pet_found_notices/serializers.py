from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.pet_found_notices.models import PetFoundNotice


class PetFoundNoticeSerializer(ModelSerializer):
    finder = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault()),
        required=False,
    )

    class Meta:
        model = PetFoundNotice
        fields = (
            'id',
            'finder',
            'status',
            'title',
            'description',
            'pet_name',
            'pet_species',
            'pet_breed',
            'pet_color',
            'pet_special_marks',
            'pet_sex',
            'pet_age',
            'found_datetime',
            'found_location',
            'image',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'finder',
            'created_at',
            'updated_at',
        )
