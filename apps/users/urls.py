from apps.users.apis import (
    UserListApi,
    UserRegisterApi,
)
from django.urls import path


urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
    path("register/", UserRegisterApi.as_view(), name="register"),
]
