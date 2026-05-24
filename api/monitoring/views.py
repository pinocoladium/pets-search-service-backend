from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from apps.monitoring.collectors import update_business_metrics


def metrics_view(request):
    """Возвращает метрики приложения в формате Prometheus."""
    update_business_metrics()

    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )
