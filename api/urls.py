from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # APIs
    path('users/', include('api.users.urls')),
    path('complaints/', include('api.complaints.urls')),
    path('communications/', include('api.communications.urls')),
    path('pet-adoption-notices/', include('api.pet_adoption_notices.urls')),
    path('pet-missing-notices/', include('api.pet_missing_notices.urls')),
    path('pet-found-notices/', include('api.pet_found_notices.urls')),
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]
