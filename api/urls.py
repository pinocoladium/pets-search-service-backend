from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # APIs
    path('users/', include('api.users.urls')),
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]
