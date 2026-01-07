from django.db.models import TextChoices


class PetFoundNoticeStatusChoices(TextChoices):
    NEW = 'NEW', 'Новое'
    ACTIVE = 'ACTIVE', 'Активное'
    RETURNED = 'RETURNED', 'Питомец возвращен'
    CLOSED = 'CLOSED', 'Закрыто'
    BLOCKED = 'BLOCKED', 'Заблокировано'
