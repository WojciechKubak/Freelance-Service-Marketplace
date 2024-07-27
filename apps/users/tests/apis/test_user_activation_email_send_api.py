from apps.users.apis import UserActivationEmailSendApi
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
import pytest


class TestUserActivationEmailSendApi:

    @pytest.mark.django_db
    def test_api_response_on_already_activated_user(self) -> None:
        user = UserFactory(is_active=True)

        factory = APIRequestFactory()
        request = factory.post(
            "/api/users/activation-email-resend/", {"email": user.email}
        )

        response = UserActivationEmailSendApi.as_view()(request)

        assert 200 == response.status_code
        assert {"email": user.email} == response.data

    @pytest.mark.django_db
    def test_api_response_on_successful_activation_email_send(self) -> None:
        user = UserFactory(is_active=False)

        factory = APIRequestFactory()
        request = factory.post(
            "/api/users/activation-email-resend/", {"email": user.email}
        )

        response = UserActivationEmailSendApi.as_view()(request)

        assert 200 == response.status_code
        assert {"email": user.email} == response.data
