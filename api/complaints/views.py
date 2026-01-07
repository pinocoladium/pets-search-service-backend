from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from api.complaints.serializers import ComplaintSerializer
from apps.complaints.models import Complaint
from utils.views import NoDeleteModelViewSet


class ComplaintViewSet(NoDeleteModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('status',)

    def update(self, request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_admin:
            return queryset
        return queryset.filter(creator=self.request.user)
