from apps.consultations.apis import (
    ConsultationCreateApi,
    ConsultationUpdateApi,
    ConsultationChangeVisibilityApi,
    ConsultationListApi,
    ConsultationDetailApi,
)
from django.urls import path, include


consultation_patterns = [
    path("", ConsultationListApi.as_view(), name="list"),
    path("<int:consultation_id>/", ConsultationDetailApi.as_view(), name="detail"),
    path("create/", ConsultationCreateApi.as_view(), name="create"),
    path(
        "<int:consultation_id>/update/", ConsultationUpdateApi.as_view(), name="update"
    ),
    path(
        "<int:consultation_id>/change-visibility/",
        ConsultationChangeVisibilityApi.as_view(),
        name="change-visibility",
    ),
]

urlpatterns = [
    path(
        "",
        include((consultation_patterns, "consultations"), namespace="consultations"),
    ),
]
