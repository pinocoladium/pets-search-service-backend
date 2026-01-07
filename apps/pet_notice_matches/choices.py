from django.db.models import TextChoices


class PetNoticeMatchStatusChoices(TextChoices):
    PENDING = 'PENDING', 'Ожидает рассмотрения'
    APPROVED = 'APPROVED', 'Подтверждено совпадение'
    DECLINED = 'DECLINED', 'Отклонено'
