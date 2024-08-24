from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from unittest.mock import Mock, MagicMock, patch
import pytest


class TestUserResetPasswordEmailSend:
    user_service = UserService()

    @pytest.mark.django_db
    @patch("apps.users.services.send_password_reset_email")
    def test_function_on_failed_due_to_non_existing_user(
        self, mock_send_password_reset_email: Mock
    ) -> None:
        result = self.user_service.user_reset_password_email_send(
            email="user@example.com"
        )

        mock_send_password_reset_email.assert_not_called()

        assert "user@example.com" == result

    @pytest.mark.django_db
    @patch("apps.users.services.send_password_reset_email")
    def test_function_on_failed_due_to_inactive_user(
        self, mock_send_password_reset_email: Mock
    ) -> None:
        user = UserFactory(is_active=False)

        result = self.user_service.user_reset_password_email_send(email=user.email)

        mock_send_password_reset_email.assert_not_called()

        assert user.email == result

    @pytest.mark.django_db
    @patch("apps.users.services.send_password_reset_email")
    def test_service_method_sucesfully_sends_password_reset_email(
        self, mock_send_password_reset_email: MagicMock
    ) -> None:
        user = UserFactory(is_active=True)

        result = self.user_service.user_reset_password_email_send(email=user.email)

        mock_send_password_reset_email.assert_called_once_with(
            user_email=user.email,
            url=self.user_service.url_generate(
                user_id=user.id, viewname="api:users:user-reset"
            ),
        )

        assert user.email == result
