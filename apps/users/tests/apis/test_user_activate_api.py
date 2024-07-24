from apps.users.tests.factories import UserFactory
from apps.users.apis import UserActivateApi
from django.core.signing import TimestampSigner
from rest_framework.test import APIRequestFactory
import pytest
import uuid


def sign_value(value: str) -> str:
    signer = TimestampSigner()
    return signer.sign(value)


class TestUserActivateApi:

    def test_api_response_on_failed_due_to_signature_error(self) -> None:
        signed_id = sign_value(uuid.uuid4())[:-1]

        factory = APIRequestFactory()
        request = factory.post("api/users/activate/")

        response = UserActivateApi.as_view()(request, signed_id=signed_id)

        assert 400 == response.status_code

    @pytest.mark.django_db
    def test_api_response_on_successfull_user_activation(self) -> None:
        user = UserFactory(is_active=False)

        signed_id = sign_value(str(user.id))

        factory = APIRequestFactory()
        request = factory.post("api/users/activate/")

        response = UserActivateApi.as_view()(request, signed_id=signed_id)

        assert 200 == response.status_code
