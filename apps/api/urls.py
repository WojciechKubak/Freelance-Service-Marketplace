from django.urls import path, include


urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("users/", include("apps.users.urls")),
    path("categorization/", include("apps.categorization.urls")),
    path("consultations/", include("apps.consultations.urls")),
]
