from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.users.serializers import UserLocationSerializer, UserSerializer
from apps.users.models import UserLocation


User = get_user_model()


class CreateUserAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Создание пользователя',
        description='Создать пользователя',
        request=serializer_class,
        responses={status.HTTP_201_CREATED: serializer_class},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(**serializer.validated_data)
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)


class UserAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        summary='Получение пользователя',
        description='Получить пользователя',
        request=serializer_class,
        responses={status.HTTP_200_OK: serializer_class},
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        user = self.get_queryset().get(id=request.user.id)
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Изменение пользователя',
        description='Изменить пользователя',
        request=serializer_class,
        responses={status.HTTP_200_OK: serializer_class},
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        user = request.user

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.pop('password', None)

        for attr, value in serializer.validated_data.items():
            setattr(user, attr, value)

        if password:
            user.set_password(password)

        user.save()

        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)


class UserLocationAPIView(GenericAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer

    @extend_schema(
        summary='Создание локации пользователя',
        description='Создать локации пользователя',
        request=serializer_class,
        responses={status.HTTP_201_CREATED: serializer_class},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='Получение локации пользователя',
        description='Получить локации пользователя',
        request=serializer_class,
        responses={status.HTTP_200_OK: serializer_class(many=True)},
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        locations = self.get_queryset().filter(user=request.user)
        return Response(self.get_serializer(locations, many=True).data, status=status.HTTP_200_OK)
