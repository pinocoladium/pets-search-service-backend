from django.urls import path

from api.ai.views import OllamaGenerateResponseAPIView, OllamaImageDescriptionAPIView


urlpatterns = [
    path('ollama/', OllamaGenerateResponseAPIView.as_view(), name='ollama-generate-response'),
    path('ollama/image-description/', OllamaImageDescriptionAPIView.as_view(), name='ollama-image-description'),
]
