from apps.users.apis import UserResetPasswordApi
from apps.users.services import sign_user_id
from apps.users.tests.factories import UserFactory
from apps.users.services import USER_PASSWORD_RESET_LINK_INVALID, USER_NOT_ACTIVE
from rest_framework.test import APIRequestFactory
from collections import OrderedDict


class TestUserResetPasswordApi:
    url = "/api/users/reset/"

    def test_api_response_on_failed_due_to_missing_required_fields(self) -> None:
        request = APIRequestFactory().post(self.url)

        response = UserResetPasswordApi.as_view()(request, signed_id="some-signed-id")

        expected_response_data = OrderedDict(
            {
                "detail": {
                    "password": ["This field is required."],
                }
            }
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_failed_due_to_invalid_signed_user_id(self) -> None:
        factory = APIRequestFactory()
        request = factory.post(self.url, {"password": "12345"})

        response = UserResetPasswordApi.as_view()(
            request, signed_id="invalid-signed-id"
        )

        expected_response_data = OrderedDict(
            {"detail": {"non_field_errors": [USER_PASSWORD_RESET_LINK_INVALID]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_failed_due_to_inactive_user(self) -> None:
        user = UserFactory(is_active=False)
        signed_id = sign_user_id(str(user.id))

        factory = APIRequestFactory()
        request = factory.post(self.url, {"value": signed_id, "password": "12345"})

        response = UserResetPasswordApi.as_view()(request, signed_id=signed_id)

        expected_response_data = OrderedDict(
            {"detail": {"non_field_errors": [USER_NOT_ACTIVE]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_password_reset(self) -> None:
        user = UserFactory(is_active=True)
        signed_id = sign_user_id(str(user.id))

        factory = APIRequestFactory()
        request = factory.post(self.url, {"value": signed_id, "password": "12345"})

        response = UserResetPasswordApi.as_view()(request, signed_id=signed_id)

        expected_response_data = OrderedDict({"id": str(user.id), "email": user.email})

        assert 200 == response.status_code
        assert expected_response_data == response.data
