from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pet_found_notices.serializers import PetFoundNoticeSerializer
from apps.pet_found_notices.choices import PetFoundNoticeStatusChoices
from apps.pet_found_notices.models import PetFoundNotice
from utils.constants import NEAREST_NOTICE_DISTANCE_IN_METERS
from utils.serializers import NoticeLocationSerializer
from utils.views import NoDeleteModelViewSet


class ActivePetFoundNoticeAPIView(ReadOnlyModelViewSet):
    queryset = PetFoundNotice.objects.filter(status=PetFoundNoticeStatusChoices.ACTIVE)
    serializer_class = PetFoundNoticeSerializer
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
            queryset = queryset.filter(found_location__distance_lte=(point, NEAREST_NOTICE_DISTANCE_IN_METERS))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PetFoundNoticeViewSet(NoDeleteModelViewSet):
    queryset = PetFoundNotice.objects.all()
    serializer_class = PetFoundNoticeSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('status',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not (request.user.is_admin or instance.finder == request.user):
            raise PermissionDenied

        return super().update(request, *args, **kwargs)


class CreateAnonymousPetFoundNoticeAPIView(GenericAPIView):
    queryset = PetFoundNotice.objects.all()
    serializer_class = PetFoundNoticeSerializer

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Создание анонимного объявления о находке',
        description='Создать анонимное объявления о находке',
        request=serializer_class,
        responses={status.HTTP_201_CREATED: serializer_class},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pet_found_notice = PetFoundNotice(**serializer.validated_data | {'finder': None})
        pet_found_notice.save()

        return Response(self.get_serializer(pet_found_notice).data, status=status.HTTP_201_CREATED)
