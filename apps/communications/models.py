from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Notification(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        related_name='notifications',
    )

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=30,
    )

    text = models.CharField(
        verbose_name='Текст',
        max_length=100,
    )

    is_read = models.BooleanField(
        verbose_name='Прочитано',
        default=False,
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Message(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        related_name='messages',
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Отправитель',
        related_name='sent_messages',
    )

    text = models.CharField(
        verbose_name='Текст',
        max_length=100,
    )

    is_read = models.BooleanField(
        verbose_name='Прочитано',
        default=False,
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
