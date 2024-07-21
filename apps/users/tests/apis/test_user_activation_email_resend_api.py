from apps.users.apis import UserActivationEmailResendApi
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
import pytest


class TestUserActivationEmailResendApi:

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_already_active_user(self) -> None:
        user = UserFactory(is_active=True)

        factory = APIRequestFactory()
        request = factory.post(
            "/api/users/activation-email-resend/", {"email": user.email}
        )

        response = UserActivationEmailResendApi.as_view()(request)

        assert 400 == response.status_code

    @pytest.mark.django_db
    def test_api_response_on_successful_resend(self) -> None:
        user = UserFactory(is_active=False)

        factory = APIRequestFactory()
        request = factory.post(
            "/api/users/activation-email-resend/", {"email": user.email}
        )

        response = UserActivationEmailResendApi.as_view()(request)

        assert 200 == response.status_code
