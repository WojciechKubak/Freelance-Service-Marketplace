from apps.api.apis import HealthCheckAPI
from django.urls import path


urlpatterns = [
    path("health/", HealthCheckAPI.as_view(), name="health-check"),
]
