from django.urls import path, include


consultation_patterns = []

urlpatterns = [
    path(
        "",
        include((consultation_patterns, "consultations"), namespace="consultations"),
    ),
]
