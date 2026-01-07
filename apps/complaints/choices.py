from django.db.models import TextChoices


class ComplaintStatusChoices(TextChoices):
    NEW = 'NEW', 'Новое'
    COMPLETED = 'COMPLETED', 'Выполнено'
    DECLINED = 'DECLINED', 'Отклонено'


class ComplaintObjectTypeChoices(TextChoices):
    USER = 'USER', 'Пользователь'
    MISSING_NOTICE = 'MISSING_NOTICE', 'Объявление о пропаже питомца'
    FOUND_NOTICE = 'FOUND_NOTICE', 'Объявление о находке питомца'
    ADOPTION_NOTICE = 'ADOPTION_NOTICE', 'Объявление о пристройстве питомца'
