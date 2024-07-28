from apps.users.tests.factories import UserFactory
from apps.users.apis import UserSignupApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestUserSignupApi:
    url: str = "api/users/signup/"

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_missing_required_field(self) -> None:
        request = APIRequestFactory().post(
            self.url,
            {"password": "password"},
        )
        response = UserSignupApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"email": ["This field is required."]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_unique_email_constraint(self) -> None:
        email = "user@example.com"
        UserFactory(email=email)

        request = APIRequestFactory().post(
            self.url,
            {"email": email, "password": "password"},
        )
        response = UserSignupApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"email": ["User with this Email address already exists."]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successful_signup(self) -> None:
        email = "user@example.com"

        request = APIRequestFactory().post(
            self.url,
            {"email": email, "password": "password"},
        )

        response = UserSignupApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "email": email,
                "is_admin": False,
                "is_active": False,
            }
        )

        assert 201 == response.status_code
        assert expected_response_data == response.data
