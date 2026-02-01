from rest_framework.routers import SimpleRouter

from api.communications.views import MessageViewSet, NotificationViewSet


router = SimpleRouter()

router.register('notifications', NotificationViewSet)
router.register('messages', MessageViewSet)

urlpatterns = router.urls
