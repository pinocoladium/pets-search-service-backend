from django.contrib.auth import get_user_model

from apps.communications.models import Message, Notification
from apps.complaints.models import Complaint
from apps.monitoring.metrics import (
    complaints_total,
    pet_adoption_notices_total,
    pet_found_notices_total,
    pet_missing_notices_total,
    pet_notice_matches_total,
    unread_messages_total,
    unread_notifications_total,
    users_total,
)
from apps.pet_adoption_notices.models import PetAdoptionNotice
from apps.pet_found_notices.models import PetFoundNotice
from apps.pet_missing_notices.models import PetMissingNotice
from apps.pet_notice_matches.models import PetNoticeMatch


User = get_user_model()


def update_business_metrics() -> None:
    """Обновляет бизнес-метрики проекта перед отдачей /metrics."""
    pet_missing_notices_total.set(PetMissingNotice.objects.count())
    pet_found_notices_total.set(PetFoundNotice.objects.count())
    pet_adoption_notices_total.set(PetAdoptionNotice.objects.count())
    pet_notice_matches_total.set(PetNoticeMatch.objects.count())
    complaints_total.set(Complaint.objects.count())
    unread_notifications_total.set(Notification.objects.filter(is_read=False).count())
    unread_messages_total.set(Message.objects.filter(is_read=False).count())
    users_total.set(User.objects.count())
