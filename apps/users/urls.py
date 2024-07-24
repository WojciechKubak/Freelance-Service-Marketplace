from apps.users.apis import (
    UserListApi,
    UserRegisterApi,
    UserActivateApi,
    UserActivationEmailSendApi,
    UserResetPasswordApi,
    UserResetPasswordEmailSendApi,
)
from django.urls import path


urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
    path("register/", UserRegisterApi.as_view(), name="register"),
    path("activate/<str:signed_id>/", UserActivateApi.as_view(), name="activate"),
    path(
        "activation-email-resend/",
        UserActivationEmailSendApi.as_view(),
        name="activation-email-resend",
    ),
    path(
        "reset-password//<str:signed_id>/",
        UserResetPasswordApi.as_view(),
        name="password-reset",
    ),
    path(
        "reset-password-email-send/",
        UserResetPasswordEmailSendApi.as_view(),
        name="reset-password-email-send",
    ),
]
