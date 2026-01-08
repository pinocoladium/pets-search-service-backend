from rest_framework.routers import SimpleRouter

from api.pet_missing_notices.views import ActivePetMissingNoticeAPIView, PetMissingNoticeViewSet


router = SimpleRouter()

router.register('active', ActivePetMissingNoticeAPIView, basename='activepetmissingnotice')
router.register('', PetMissingNoticeViewSet)

urlpatterns = router.urls
