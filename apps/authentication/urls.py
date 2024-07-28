from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include


auth_patterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]

urlpatterns = [
    path("", include((auth_patterns, "auth"), namespace="auth")),
]
