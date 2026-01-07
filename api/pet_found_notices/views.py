from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.pet_found_notices.serializers import PetFoundNoticeSerializer
from apps.pet_found_notices.models import PetFoundNotice
from utils.views import NoDeleteModelViewSet


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
