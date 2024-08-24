from apps.users.tests.factories import UserFactory
from apps.users.apis import UserListApi
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestUserListApi:
    url: str = "api/users/"

    def test_api_returns_no_results_with_filter_provided(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_admin=True, is_active=True)

        url = f"{self.url}?email=other_{user.email}"

        request = auth_request(user=user, method="GET", url=url)
        response = UserListApi.as_view()(request)

        expected_response_results = OrderedDict(
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [],
            }
        )

        assert expected_response_results == response.data

    def test_api_returns_single_results_with_filter_provided(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_admin=True, is_active=True)

        url = f"{self.url}?email={user.email}"

        request = auth_request(user=user, method="GET", url=url)
        response = UserListApi.as_view()(request)

        expected_response_results = OrderedDict(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": str(user.id),
                        "email": user.email,
                        "is_admin": user.is_admin,
                        "is_active": user.is_active,
                    }
                ],
            }
        )

        assert expected_response_results == response.data

    def test_api_returns_all_results_without_filters_provided(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        auth_user = UserFactory(is_admin=True, is_active=True)

        user1 = UserFactory(is_active=False)
        user2 = UserFactory(is_active=False)

        url = f"{self.url}?is_active=False"

        request = auth_request(user=auth_user, method="GET", url=url)
        response = UserListApi.as_view()(request)

        expected_response_results = OrderedDict(
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": str(user1.id),
                        "email": user1.email,
                        "is_admin": user1.is_admin,
                        "is_active": user1.is_active,
                    },
                    {
                        "id": str(user2.id),
                        "email": user2.email,
                        "is_admin": user2.is_admin,
                        "is_active": user2.is_active,
                    },
                ],
            }
        )

        assert expected_response_results == response.data
