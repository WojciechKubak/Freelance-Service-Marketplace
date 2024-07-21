from apps.users.apis import (
    UserListApi,
    UserRegisterApi,
    UserActivateApi,
    UserActivationEmailResendApi,
)
from django.urls import path


urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
    path("register/", UserRegisterApi.as_view(), name="register"),
    path("activate/<str:user_id>/", UserActivateApi.as_view(), name="activate"),
    path(
        "activation-email-resend/",
        UserActivationEmailResendApi.as_view(),
        name="activation-email-resend",
    ),
]
