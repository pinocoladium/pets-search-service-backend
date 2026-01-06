from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class NoDeleteModelViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    pass
