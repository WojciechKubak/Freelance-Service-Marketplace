from apps.users.models import User
from apps.users.apis import UserPasswordChangeApi
from apps.users.services import USER_INVALID_PASSWORD, USER_INVALID_PASSWORD_CONFIRM
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestUserPasswordChangeApi:
    url: str = "/api/users/change-password/"

    def test_api_response_on_failed_due_to_missing_required_fields(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        request = auth_request(user, "POST", self.url, data={})

        response = UserPasswordChangeApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "detail": {
                    "password": ["This field is required."],
                    "new_password": ["This field is required."],
                    "new_password_confirm": ["This field is required."],
                }
            }
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_failed_due_to_incorrect_password(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        request_data = {
            "password": "password_incorrect",
            "new_password": "new_password",
            "new_password_confirm": "new_password",
        }
        request = auth_request(user, "POST", self.url, data=request_data)

        response = UserPasswordChangeApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"non_field_errors": [USER_INVALID_PASSWORD]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_failed_due_to_incorrect_password_repeat(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        request_data = {
            "password": "password",
            "new_password": "new_password",
            "new_password_confirm": "new_password_incorrect",
        }
        request = auth_request(user, "POST", self.url, data=request_data)

        response = UserPasswordChangeApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"non_field_errors": [USER_INVALID_PASSWORD_CONFIRM]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_password_change(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        request_data = {
            "password": "password",
            "new_password": "new_password",
            "new_password_confirm": "new_password",
        }
        request = auth_request(user, "POST", self.url, data=request_data)

        response = UserPasswordChangeApi.as_view()(request)

        expected_response_data = OrderedDict({"id": str(user.id), "email": user.email})

        assert 200 == response.status_code
        assert expected_response_data == response.data
