from django.db import models

from utils.models.choices import PetSexChoices, PetSpeciesChoices


class MetadataMixin(models.Model):
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


class PetNoticeMixin(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=50,
    )

    description = models.CharField(
        verbose_name='Описание',
        max_length=150,
    )

    pet_name = models.CharField(
        verbose_name='Кличка питомца',
        max_length=30,
    )

    pet_species = models.CharField(
        verbose_name='Вид питомца',
        choices=PetSpeciesChoices.choices,
        max_length=5,
    )

    pet_breed = models.CharField(
        verbose_name='Порода питомца',
        max_length=30,
        blank=True,
    )

    pet_color = models.CharField(
        verbose_name='Окрас питомца',
        max_length=30,
    )

    pet_special_marks = models.CharField(
        verbose_name='Особые приметы питомца',
        max_length=100,
        blank=True,
    )

    pet_sex = models.CharField(
        verbose_name='Пол питомца',
        choices=PetSexChoices.choices,
        max_length=7,
    )

    pet_age = models.IntegerField(
        verbose_name='Возраст питомца',
        null=True,
    )

    class Meta:
        abstract = True
