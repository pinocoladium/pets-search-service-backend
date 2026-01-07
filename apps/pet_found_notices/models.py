from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.pet_found_notices.choices import PetFoundNoticeStatusChoices
from utils.constants import IMAGES_EXTENSIONS
from utils.models import MetadataMixin, PetNoticeMixin
from utils.validators import MaxFileSizeValidator


User = get_user_model()


class PetFoundNotice(PetNoticeMixin, MetadataMixin):
    status = models.CharField(
        verbose_name='Статус',
        choices=PetFoundNoticeStatusChoices.choices,
        default=PetFoundNoticeStatusChoices.NEW,
        max_length=8,
    )

    finder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Нашедший',
        related_name='pet_found_notices',
        null=True,
    )

    found_datetime = models.DateTimeField(
        verbose_name='Время находки питомца',
    )

    found_location = PointField(
        verbose_name='Местоположение питомца',
    )

    image = models.FileField(
        verbose_name='Фотография',
        upload_to='pet-found-notices-photos',
        validators=[
            MaxFileSizeValidator(15 * 1024 * 1024),
            FileExtensionValidator(IMAGES_EXTENSIONS),
        ],
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Объявление о находке питомца'
        verbose_name_plural = 'Объявления о находке питомца'
