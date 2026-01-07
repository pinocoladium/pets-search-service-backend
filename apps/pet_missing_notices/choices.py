from django.db.models import TextChoices


class PetMissingNoticeStatusChoices(TextChoices):
    NEW = 'NEW', 'Новое'
    ACTIVE = 'ACTIVE', 'Активное'
    FOUND = 'FOUND', 'Питомец найден'
    CLOSED = 'CLOSED', 'Закрыто'
    BLOCKED = 'BLOCKED', 'Заблокировано'
