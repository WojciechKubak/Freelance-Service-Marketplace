from apps.api.apis import HealthCheckAPI
from django.urls import path, include

urlpatterns = [
    path("health/", HealthCheckAPI.as_view(), name="health_check"),
    path("auth/", include("apps.authentication.urls")),
    path("users/", include("apps.users.urls")),
]
