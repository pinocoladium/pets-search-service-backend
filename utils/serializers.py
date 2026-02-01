from django.contrib.gis.geos import Point
from rest_framework import serializers


class NoticeLocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField(label='Долгота')
    latitude = serializers.FloatField(label='Широта')

    point = serializers.SerializerMethodField(read_only=True)

    def get_point(self, obj=None):
        """
        Превращаем валидированные координаты в Point
        """
        if 'longitude' in self.validated_data and 'latitude' in self.validated_data:
            return Point(self.validated_data['longitude'], self.validated_data['latitude'], srid=4326)
        return None
