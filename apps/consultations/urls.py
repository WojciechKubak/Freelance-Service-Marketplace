from apps.consultations.apis.consultation_api import (
    ConsultationCreateApi,
    ConsultationUpdateApi,
    ConsultationChangeVisibilityApi,
    ConsultationListApi,
    ConsultationDetailApi,
)
from apps.consultations.apis.slot_api import (
    SlotCreateApi,
    SlotUpdateApi,
    SlotDeleteApi,
    SlotListApi,
    SlotDetailApi,
)
from apps.consultations.apis.booking_api import (
    BookingCreateApi,
    BookingListApi,
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

slot_patterns = [
    path("", SlotListApi.as_view(), name="list"),
    path("<int:slot_id>/", SlotDetailApi.as_view(), name="detail"),
    path("create/", SlotCreateApi.as_view(), name="create"),
    path("<int:slot_id>/update/", SlotUpdateApi.as_view(), name="update"),
    path("<int:slot_id>/delete/", SlotDeleteApi.as_view(), name="delete"),
]

booking_patterns = [
    path("create/", BookingCreateApi.as_view(), name="create"),
    path("", BookingListApi.as_view(), name="list"),
]

urlpatterns = [
    path(
        "",
        include((consultation_patterns, "consultations"), namespace="consultations"),
    ),
    path("slots/", include((slot_patterns, "slots"), namespace="slots")),
    path("bookings/", include((booking_patterns, "bookings"), namespace="bookings")),
]
