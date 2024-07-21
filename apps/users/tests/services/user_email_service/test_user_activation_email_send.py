from apps.users.tests.factories import UserFactory
from apps.users.utils import url_generate
from apps.users.services import UserEmailService
from django.core.exceptions import ValidationError
from unittest.mock import patch
import pytest


class TestUserActivationEmailSend:

    @pytest.mark.django_db
    def test_user_activation_email_send_fails_on_already_active_user(self) -> None:
        user = UserFactory(is_active=True)

        with pytest.raises(ValidationError):
            UserEmailService.user_activation_email_send(email=user.email)

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_activation_email_send_sucesfully_resends_email(
        self, mock_send_activation_email
    ) -> None:
        user = UserFactory(is_active=False)

        UserEmailService.user_activation_email_send(email=user.email)

        mock_send_activation_email.assert_called_once_with(
            user_email=user.email,
            url=url_generate(user_id=user.id, viewname="activate"),
        )
