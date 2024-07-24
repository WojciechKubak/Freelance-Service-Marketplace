from apps.users.tests.factories import UserFactory
from apps.users.utils import url_generate
from apps.users.services import UserEmailService
from unittest.mock import Mock, MagicMock, patch
import pytest


class TestUserResetPasswordEmailSend:

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_password_reset_email")
    def test_function_on_failed_due_to_non_existing_user(
        self, mock_send_password_reset_email: Mock
    ) -> None:
        result = UserEmailService.user_reset_password_email_send(
            email="user@example.com"
        )

        mock_send_password_reset_email.assert_not_called()
        assert "user@example.com" == result

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_password_reset_email")
    def test_function_on_failed_due_to_inactive_user(
        self, mock_send_password_reset_email: Mock
    ) -> None:
        user = UserFactory(is_active=False)

        result = UserEmailService.user_reset_password_email_send(email=user.email)

        mock_send_password_reset_email.assert_not_called()
        assert user.email == result

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_password_reset_email")
    def test_service_method_sucesfully_sends_password_reset_email(
        self, mock_send_password_reset_email: MagicMock
    ) -> None:
        user = UserFactory(is_active=True)

        result = UserEmailService.user_reset_password_email_send(email=user.email)

        mock_send_password_reset_email.assert_called_once_with(
            user_email=user.email,
            url=url_generate(user_id=user.id, viewname="password-reset"),
        )
        assert user.email == result
