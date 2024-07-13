from apps.users.apis import UserListApi
from django.urls import path


urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
]
