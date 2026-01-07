from django.contrib.auth import get_user_model
from django.db import models

from apps.complaints.choices import ComplaintObjectTypeChoices, ComplaintStatusChoices
from utils.models import MetadataMixin


User = get_user_model()


class Complaint(MetadataMixin):
    status = models.CharField(
        verbose_name='Статус',
        choices=ComplaintStatusChoices.choices,
        default=ComplaintStatusChoices.NEW,
        max_length=9,
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель',
        related_name='complaints',
    )

    object_type = models.CharField(
        verbose_name='Тип объекта',
        choices=ComplaintObjectTypeChoices.choices,
        max_length=15,
    )

    object_id = models.BigIntegerField(
        verbose_name='ID объекта',
    )

    text = models.CharField(
        verbose_name='Текст',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
