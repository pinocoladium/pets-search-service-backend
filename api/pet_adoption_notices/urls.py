from rest_framework.routers import SimpleRouter

from api.pet_adoption_notices.views import PetAdoptionNoticeViewSet


router = SimpleRouter()

router.register('', PetAdoptionNoticeViewSet)

urlpatterns = router.urls
