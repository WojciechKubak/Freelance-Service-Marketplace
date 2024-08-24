from apps.users.apis import UserActivationEmailSendApi
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
import pytest


@pytest.mark.django_db
def test_api_response_on_successful_activation_email_send() -> None:
    user = UserFactory(is_active=False)

    factory = APIRequestFactory()
    request = factory.post(
        "/api/users/emails/resend-activation/", {"email": user.email}
    )

    response = UserActivationEmailSendApi.as_view()(request)

    assert 200 == response.status_code
    assert {"email": user.email} == response.data
