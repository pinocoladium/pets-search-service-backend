from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.pet_adoption_notices.models import PetAdoptionNotice


class PetAdoptionNoticeSerializer(ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault()),
        required=False,
    )

    class Meta:
        model = PetAdoptionNotice
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
            'image',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'owner',
            'created_at',
            'updated_at',
        )
