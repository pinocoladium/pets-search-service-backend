from rest_framework.routers import SimpleRouter

from api.pet_missing_notices.views import PetMissingNoticeViewSet


router = SimpleRouter()

router.register('', PetMissingNoticeViewSet)

urlpatterns = router.urls
