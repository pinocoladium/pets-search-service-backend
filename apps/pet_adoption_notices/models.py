from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.pet_adoption_notices.choices import PetAdoptionNoticeStatusChoices
from apps.pet_adoption_notices.validators import MaxFileSizeValidator
from utils.constants import IMAGES_EXTENSIONS
from utils.models import MetadataMixin, PetNoticeMixin


User = get_user_model()


class PetAdoptionNotice(PetNoticeMixin, MetadataMixin):
    status = models.CharField(
        verbose_name='Статус',
        choices=PetAdoptionNoticeStatusChoices.choices,
        default=PetAdoptionNoticeStatusChoices.NEW,
        max_length=7,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='pet_adoption_notices',
    )

    image = models.FileField(
        verbose_name='Фотография',
        upload_to='pet-adoption-notices-photos',
        validators=[
            MaxFileSizeValidator(15 * 1024 * 1024),
            FileExtensionValidator(IMAGES_EXTENSIONS),
        ],
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Объявление о пристройстве питомца'
        verbose_name_plural = 'Объявления о пристройстве питомца'
