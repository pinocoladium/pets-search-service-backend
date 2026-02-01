from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pet_missing_notices.serializers import PetMissingNoticeSerializer
from apps.pet_missing_notices.choices import PetMissingNoticeStatusChoices
from apps.pet_missing_notices.models import PetMissingNotice
from utils.constants import NEAREST_NOTICE_DISTANCE_IN_METERS
from utils.serializers import NoticeLocationSerializer
from utils.views import NoDeleteModelViewSet


class ActivePetMissingNoticeAPIView(ReadOnlyModelViewSet):
    queryset = PetMissingNotice.objects.filter(status=PetMissingNoticeStatusChoices.ACTIVE)
    serializer_class = PetMissingNoticeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        if longitude and latitude:
            serializer = NoticeLocationSerializer(data={'longitude': longitude, 'latitude': latitude})
            serializer.is_valid(raise_exception=True)
            point = serializer.get_point()
            queryset = queryset.filter(lost_location__distance_lte=(point, NEAREST_NOTICE_DISTANCE_IN_METERS))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PetMissingNoticeViewSet(NoDeleteModelViewSet):
    queryset = PetMissingNotice.objects.all()
    serializer_class = PetMissingNoticeSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('status',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not (request.user.is_admin or instance.owner == request.user):
            raise PermissionDenied

        return super().update(request, *args, **kwargs)
