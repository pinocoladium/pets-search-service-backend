from django.urls import path
from rest_framework.routers import SimpleRouter

from api.pet_found_notices.views import (
    ActivePetFoundNoticeAPIView,
    CreateAnonymousPetFoundNoticeAPIView,
    PetFoundNoticeViewSet,
)


router = SimpleRouter()

router.register('active', ActivePetFoundNoticeAPIView, basename='activepetfoundnotice')
router.register('', PetFoundNoticeViewSet)

urlpatterns = [
    path('create-anonymous-notice/', CreateAnonymousPetFoundNoticeAPIView.as_view(), name='create-anonymous-notice'),
]

urlpatterns += router.urls
