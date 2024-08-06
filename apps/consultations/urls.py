from apps.consultations.apis import ConsultationCreateApi, ConsultationUpdateApi
from django.urls import path, include


consultation_patterns = [
    path("create/", ConsultationCreateApi.as_view(), name="create"),
    path(
        "<int:consultation_id>/update/", ConsultationUpdateApi.as_view(), name="update"
    ),
]

urlpatterns = [
    path(
        "",
        include((consultation_patterns, "consultations"), namespace="consultations"),
    ),
]
