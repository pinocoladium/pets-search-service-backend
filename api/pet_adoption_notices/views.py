from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from api.pet_adoption_notices.serializers import PetAdoptionNoticeSerializer
from apps.pet_adoption_notices.models import PetAdoptionNotice
from utils.views import NoDeleteModelViewSet


class PetAdoptionNoticeViewSet(NoDeleteModelViewSet):
    queryset = PetAdoptionNotice.objects.all()
    serializer_class = PetAdoptionNoticeSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('status',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not (request.user.is_admin or instance.owner == request.user):
            raise PermissionDenied

        return super().update(request, *args, **kwargs)
