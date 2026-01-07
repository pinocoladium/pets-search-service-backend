from django.contrib.auth import get_user_model
from django.db import models

from apps.pet_found_notices.models import PetFoundNotice
from apps.pet_missing_notices.models import PetMissingNotice
from apps.pet_notice_matches.choices import PetNoticeMatchStatusChoices
from utils.models import MetadataMixin


User = get_user_model()


class PetNoticeMatch(MetadataMixin):
    match_status = models.CharField(
        verbose_name='Статус',
        choices=PetNoticeMatchStatusChoices.choices,
        default=PetNoticeMatchStatusChoices.PENDING,
        max_length=8,
    )

    found_notice = models.ForeignKey(
        PetFoundNotice,
        on_delete=models.CASCADE,
        verbose_name='Объявление о находке питомца',
        related_name='pet_notice_matches',
    )

    missing_notice = models.ForeignKey(
        PetMissingNotice,
        on_delete=models.CASCADE,
        verbose_name='Объявление о пропаже питомца',
        related_name='pet_notice_matches',
    )

    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='pet_notice_matches',
        null=True,
    )

    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Совпадение объявлений о питомцах'
        verbose_name_plural = 'Совпадения объявлений о питомцах'
