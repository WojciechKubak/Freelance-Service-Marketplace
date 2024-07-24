from apps.users.apis import UserResetPasswordEmailSendApi
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestUserResetPasswordEmailSendApi:
    url = "/api/users/reset-password-email-send/"

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_missing_required_email_field(self) -> None:
        factory = APIRequestFactory()
        request = factory.post(self.url)

        response = UserResetPasswordEmailSendApi.as_view()(request)

        expected_response_data = OrderedDict(
            {"detail": {"email": ["This field is required."]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_non_existing_user(self) -> None:
        factory = APIRequestFactory()
        request = factory.post(self.url, {"email": "user@example.com"})

        response = UserResetPasswordEmailSendApi.as_view()(request)

        assert 200 == response.status_code
        assert "user@example.com" == response.data["email"]

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_inactive_user(self) -> None:
        user = UserFactory(is_active=False)

        factory = APIRequestFactory()
        request = factory.post(self.url, {"email": user.email})

        response = UserResetPasswordEmailSendApi.as_view()(request)

        assert 200 == response.status_code
        assert user.email == response.data["email"]

    @pytest.mark.django_db
    def test_api_response_on_successful_password_reset_email_send(self) -> None:
        user = UserFactory(is_active=True)

        factory = APIRequestFactory()
        request = factory.post(self.url, {"email": user.email})

        response = UserResetPasswordEmailSendApi.as_view()(request)

        assert 200 == response.status_code
        assert user.email == response.data["email"]
