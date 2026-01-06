from django.db.models import TextChoices


class PetAdoptionNoticeStatusChoices(TextChoices):
    NEW = 'NEW', 'Новое'
    ACTIVE = 'ACTIVE', 'Активное'
    ADOPTED = 'ADOPTED', 'Питомец пристроен'
    CLOSED = 'CLOSED', 'Закрыто'
    BLOCKED = 'BLOCKED', 'Заблокировано'
