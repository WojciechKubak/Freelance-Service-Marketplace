from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from unittest.mock import Mock, patch
import pytest


class TestUserActivationEmailSend:
    user_service = UserService()

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_activation_email_send_fails_on_already_active_user(
        self, mock_send_activation_email: Mock
    ) -> None:
        user = UserFactory(is_active=True)

        result = self.user_service.user_activation_email_send(email=user.email)

        mock_send_activation_email.assert_not_called()
        assert user.email == result

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_activation_email_send_sucesfully_resends_email(
        self, mock_send_activation_email
    ) -> None:
        user = UserFactory(is_active=False)

        result = self.user_service.user_activation_email_send(email=user.email)

        assert user.email == result
        mock_send_activation_email.assert_called_once_with(
            user_email=user.email,
            url=self.user_service._url_generate(user_id=user.id, viewname="activate"),
        )
