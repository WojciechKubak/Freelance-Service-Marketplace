from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from django.core.exceptions import ValidationError
from apps.users.models import User
from unittest.mock import ANY, patch
import pytest


class TestUserCreate:

    @pytest.mark.django_db
    def test_user_create_triggers_email_duplicate_error(self) -> None:
        email = "example@domain.com"
        UserFactory(email=email)

        with pytest.raises(ValidationError):
            UserService.user_create(email=email, password="password")

    @pytest.mark.django_db
    def test_user_create_sets_up_default_parameters(self) -> None:
        UserService.user_create(email="example@domain.com", password="password")

        user = User.objects.first()

        assert not user.is_admin
        assert not user.is_active

    @pytest.mark.django_db
    @patch("apps.users.services.EmailService.send_activation_email")
    def test_user_create_saves_user_to_db_and_calls_email_service(
        self, mock_send_activation_email
    ) -> None:
        UserService.user_create(email="example@domain.com", password="password")

        mock_send_activation_email.assert_called_once_with(
            user_email="example@domain.com", activation_link=ANY
        )
        assert 1 == User.objects.count()
