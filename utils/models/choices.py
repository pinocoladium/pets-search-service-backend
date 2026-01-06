from django.db.models import TextChoices


class PetSpeciesChoices(TextChoices):
    DOG = 'DOG', 'Собака'
    CAT = 'CAT', 'Кошка'
    BIRD = 'BIRD', 'Птица'
    OTHER = 'OTHER', 'Другое'


class PetSexChoices(TextChoices):
    MALE = 'MALE', 'М'
    FEMALE = 'FEMALE', 'Ж'
    UNKNOW = 'UNKNOWN', 'Неизвестно'
