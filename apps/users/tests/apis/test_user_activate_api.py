from apps.users.tests.factories import UserFactory
from apps.users.apis import UserActivateApi
from apps.users.services import USER_ACTIVATION_LINK_INVALID, sign_user_id
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import uuid


class TestUserActivateApi:
    url: str = "api/users/activate/"

    def test_api_response_on_failed_due_to_signature_error(self) -> None:
        invalid_signed_id = sign_user_id(uuid.uuid4())[:-1]

        factory = APIRequestFactory()
        request = factory.post(self.url)

        response = UserActivateApi.as_view()(request, signed_id=invalid_signed_id)

        expected_response_data = OrderedDict(
            {"detail": {"non_field_errors": [USER_ACTIVATION_LINK_INVALID]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successfull_user_activation(self) -> None:
        user = UserFactory(is_active=False)

        signed_id = sign_user_id(str(user.id))

        factory = APIRequestFactory()
        request = factory.post(self.url)

        response = UserActivateApi.as_view()(request, signed_id=signed_id)

        expected_response_data = OrderedDict(
            {"id": user.id, "email": user.email, "is_active": True}
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
