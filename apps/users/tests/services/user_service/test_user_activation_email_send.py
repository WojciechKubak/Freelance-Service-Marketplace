from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from django.core.exceptions import ValidationError
from unittest.mock import patch
import pytest


class TestUserActivationEmailSend:
    user_service = UserService()

    @pytest.mark.django_db
    def test_user_activation_email_send_fails_on_already_active_user(self) -> None:
        user = UserFactory(is_active=True)

        with pytest.raises(ValidationError):
            self.user_service.user_activation_email_send(email=user.email)

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_activation_email_send_sucesfully_resends_email(
        self, mock_send_activation_email
    ) -> None:
        user = UserFactory(is_active=False)

        self.user_service.user_activation_email_send(email=user.email)

        mock_send_activation_email.assert_called_once_with(
            user_email=user.email,
            url=self.user_service._url_generate(user_id=user.id, viewname="activate"),
        )
