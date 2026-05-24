from django.urls import path

from api.monitoring.views import metrics_view


urlpatterns = [
    path('metrics/', metrics_view, name='metrics'),
]
