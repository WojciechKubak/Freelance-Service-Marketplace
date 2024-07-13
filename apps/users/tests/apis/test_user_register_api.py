from apps.users.apis import UserRegisterApi
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestUserRegisterApi:

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_missing_required_field(self) -> None:
        request = APIRequestFactory().post(
            "/api/users/register/",
            {"password": "password"},
        )
        response = UserRegisterApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"email": ["This field is required."]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_unique_email_constraint(self) -> None:
        email = "user@example.com"
        User.objects.create_user(email=email, password="password")

        request = APIRequestFactory().post(
            "/api/users/register/",
            {"email": email, "password": "password"},
        )
        response = UserRegisterApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"email": ["User with this Email address already exists."]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successful_registration(self) -> None:
        email = "user@example.com"

        request = APIRequestFactory().post(
            "/api/users/register/",
            {"email": email, "password": "password"},
        )

        response = UserRegisterApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "email": email,
                "is_admin": False,
                "is_active": True,
            }
        )

        assert 201 == response.status_code
        assert expected_response_data == response.data
