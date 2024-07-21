from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from django.core.exceptions import ValidationError
from unittest.mock import patch
import pytest


class TestUserActivationEmailResend:

    @pytest.mark.django_db
    def test_user_activation_email_resend_fails_on_already_active_user(self) -> None:
        user = UserFactory(is_active=True)

        with pytest.raises(ValidationError):
            UserService.user_activation_email_resend(email=user.email)

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_activation_email_resend_sucesfully_resends_email(
        self, mock_send_activation_email
    ) -> None:
        user = UserFactory(is_active=False)

        UserService.user_activation_email_resend(email=user.email)

        mock_send_activation_email.assert_called_once_with(
            user_email=user.email,
            activation_link=UserService._activation_link_create(user_id=user.id),
        )
