from django.db import models


class MetadataModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name='Время обновления',
        auto_now=True,
    )

    class Meta:
        abstract = True
