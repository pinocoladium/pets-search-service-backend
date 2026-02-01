from rest_framework.routers import SimpleRouter

from api.complaints.views import ComplaintViewSet


router = SimpleRouter()

router.register('', ComplaintViewSet)

urlpatterns = router.urls
