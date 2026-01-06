from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import token_obtain_pair

from api.users import views


router = SimpleRouter()

urlpatterns = [
    path('token/', token_obtain_pair),
    path('me/', views.UserAPIView.as_view(), name='user'),
    path('me/locations/', views.UserLocationAPIView.as_view(), name='user-locations'),
    path('create/', views.CreateUserAPIView.as_view(), name='create-user'),
]

urlpatterns += router.urls
