from prometheus_client import Gauge


pet_missing_notices_total = Gauge(
    'pet_missing_notices_total',
    'Current number of missing pet notices',
)

pet_found_notices_total = Gauge(
    'pet_found_notices_total',
    'Current number of found pet notices',
)

pet_adoption_notices_total = Gauge(
    'pet_adoption_notices_total',
    'Current number of pet adoption notices',
)

pet_notice_matches_total = Gauge(
    'pet_notice_matches_total',
    'Current number of matches between missing and found notices',
)

complaints_total = Gauge(
    'complaints_total',
    'Current number of complaints',
)

unread_notifications_total = Gauge(
    'unread_notifications_total',
    'Current number of unread notifications',
)

unread_messages_total = Gauge(
    'unread_messages_total',
    'Current number of unread messages',
)

users_total = Gauge(
    'users_total',
    'Current number of users',
)
