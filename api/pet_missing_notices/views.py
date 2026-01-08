from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pet_missing_notices.serializers import PetMissingNoticeSerializer
from apps.pet_missing_notices.choices import PetMissingNoticeStatusChoices
from apps.pet_missing_notices.models import PetMissingNotice
from utils.views import NoDeleteModelViewSet


class ActivePetMissingNoticeAPIView(ReadOnlyModelViewSet):
    queryset = PetMissingNotice.objects.filter(status=PetMissingNoticeStatusChoices.ACTIVE)
    serializer_class = PetMissingNoticeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


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
