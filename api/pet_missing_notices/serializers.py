from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.pet_missing_notices.models import PetMissingNotice


class PetMissingNoticeSerializer(ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault()),
        required=False,
    )

    class Meta:
        model = PetMissingNotice
        fields = (
            'id',
            'owner',
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
            'lost_datetime',
            'lost_location',
            'image',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'owner',
            'created_at',
            'updated_at',
        )
