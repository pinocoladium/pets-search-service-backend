from django.urls import path
from rest_framework.routers import SimpleRouter

from api.pet_found_notices.views import CreateAnonymousPetFoundNoticeAPIView, PetFoundNoticeViewSet


router = SimpleRouter()

router.register('', PetFoundNoticeViewSet)

urlpatterns = [
    path('create-anonymous-notice/', CreateAnonymousPetFoundNoticeAPIView.as_view(), name='create-anonymous-notice'),
]

urlpatterns += router.urls
