from django.urls import path

from api.ai.views import (
    OllamaCheckAnnouncementAPIView,
    OllamaGenerateAnnouncementTitleAPIView,
    OllamaGenerateResponseAPIView,
    OllamaImproveAnnouncementAPIView,
    OllamaPetDescriptionAPIView,
)


urlpatterns = [
    path('ask/', OllamaGenerateResponseAPIView.as_view(), name='ollama-ask'),
    path('pet-description/', OllamaPetDescriptionAPIView.as_view(), name='ollama-pet-description'),
    path('improve-announcement/', OllamaImproveAnnouncementAPIView.as_view(), name='ollama-improve-announcement'),
    path('generate-title/', OllamaGenerateAnnouncementTitleAPIView.as_view(), name='ollama-generate-title'),
    path('check-announcement/', OllamaCheckAnnouncementAPIView.as_view(), name='ollama-check-announcement'),
]
