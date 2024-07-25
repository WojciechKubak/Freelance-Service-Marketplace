"""
class UserPasswordChangeApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        password = serializers.CharField()
        new_password = serializers.CharField()
        new_password_confirm = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email"]

    def post(self, request: Request) -> Response:
        user = request.user

        serializer = UserPasswordChangeApi.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.user_password_change(user=user, **serializer.validated_data)

        output_serializer = UserPasswordChangeApi.OutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

"""

from apps.users.models import User
from apps.users.apis import UserPasswordChangeApi
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable
import pytest


class TestUserPasswordChangeApi:
    url: str = "/api/users/password-change/"

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_missing_required_fields(
        self,
        auth_request: Callable[[User, str, str], APIRequestFactory],
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

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_incorrect_password(
        self, auth_request: Callable[[User, str, str], APIRequestFactory]
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
            {"detail": {"non_field_errors": ["Invalid password"]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_incorrect_password_repeat(
        self, auth_request: Callable[[User, str, str], APIRequestFactory]
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
            {"detail": {"non_field_errors": ["Passwords do not match"]}}
        )

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successful_password_change(
        self, auth_request: Callable[[User, str, str], APIRequestFactory]
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
