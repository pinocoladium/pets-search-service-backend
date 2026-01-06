from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.db import models

from apps.users.validators import name_validator, phone_validator
from utils.models import MetadataMixin


class User(AbstractUser, MetadataMixin):
    is_admin = models.BooleanField(
        verbose_name='Администратор',
        default=False,
    )

    name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        validators=[name_validator],
    )

    username = models.CharField(
        verbose_name='Логин',
        max_length=50,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={'unique': 'Пользователь с таким логином уже существует'},
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        error_messages={'unique': 'Пользователь с таким email уже существует'},
    )

    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
        unique=True,
        validators=[phone_validator],
        error_messages={'unique': 'Пользователь с таким номером уже существует'},
    )

    notifications_enabled = models.BooleanField(
        verbose_name='Уведомления включены',
        default=True,
    )

    is_blocked = models.BooleanField(
        verbose_name='Заблокирован',
        default=False,
    )

    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
    )

    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    date_joined = None

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserLocation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='locations',
    )

    title = models.CharField(
        verbose_name='Наименование',
        max_length=50,
    )

    location = PointField(
        verbose_name='Местоположение',
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Местоположение пользователя'
        verbose_name_plural = 'Местоположения пользователей'
