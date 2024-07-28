from apps.users.apis import (
    UserListApi,
    UserSignupApi,
    UserActivateApi,
    UserActivationEmailSendApi,
    UserResetPasswordApi,
    UserResetPasswordEmailSendApi,
    UserPasswordChangeApi,
)
from django.urls import path, include


user_patterns = [
    path("", UserListApi.as_view(), name="user-list"),
    path("signup/", UserSignupApi.as_view(), name="user-signup"),
    path("activate/<str:signed_id>/", UserActivateApi.as_view(), name="user-activate"),
    path("reset/<str:signed_id>/", UserResetPasswordApi.as_view(), name="user-reset"),
    path(
        "change-password/", UserPasswordChangeApi.as_view(), name="user-change-password"
    ),
]

email_patterns = [
    path(
        "reset-password/",
        UserResetPasswordEmailSendApi.as_view(),
        name="reset-password",
    ),
    path(
        "resend-activation/",
        UserActivationEmailSendApi.as_view(),
        name="resend-activation",
    ),
]

urlpatterns = [
    path("", include((user_patterns, "users"), namespace="users")),
    path("emails/", include((email_patterns, "emails"), namespace="emails")),
]
