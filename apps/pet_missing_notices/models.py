from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.pet_missing_notices.choices import PetMissingNoticeStatusChoices
from utils.constants import IMAGES_EXTENSIONS
from utils.models import MetadataMixin, PetNoticeMixin
from utils.validators import MaxFileSizeValidator


User = get_user_model()


class PetMissingNotice(PetNoticeMixin, MetadataMixin):
    status = models.CharField(
        verbose_name='Статус',
        choices=PetMissingNoticeStatusChoices.choices,
        default=PetMissingNoticeStatusChoices.NEW,
        max_length=7,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='pet_missing_notices',
    )

    lost_datetime = models.DateTimeField(
        verbose_name='Время пропажи питомца',
    )

    lost_location = PointField(
        verbose_name='Последнее местоположение питомца',
    )

    image = models.FileField(
        verbose_name='Фотография',
        upload_to='pet-missing-notices-photos',
        validators=[
            MaxFileSizeValidator(15 * 1024 * 1024),
            FileExtensionValidator(IMAGES_EXTENSIONS),
        ],
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Объявление о пропаже питомца'
        verbose_name_plural = 'Объявления о пропаже питомца'
