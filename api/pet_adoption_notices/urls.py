from rest_framework.routers import SimpleRouter

from api.pet_adoption_notices.views import ActivePetAdoptionNoticeAPIView, PetAdoptionNoticeViewSet


router = SimpleRouter()

router.register('active', ActivePetAdoptionNoticeAPIView, basename='activepetadoptionnotice')
router.register('', PetAdoptionNoticeViewSet)

urlpatterns = router.urls
