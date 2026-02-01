from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.communications.serializers import MessageSerializer, NotificationSerializer
from apps.communications.models import Message, Notification


class NotificationViewSet(ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('is_read',)

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)


class MessageViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('is_read',)

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)
