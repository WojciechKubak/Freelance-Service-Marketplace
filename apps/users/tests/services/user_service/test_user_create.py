from apps.users.tests.factories import UserFactory
from apps.users.services import UserService
from django.core.exceptions import ValidationError
from apps.users.models import User
import pytest


class TestUserCreate:

    @pytest.mark.django_db
    def test_user_create_saves_user_to_database(self) -> None:
        UserService.user_create(email="example@domain.com", password="password")
        assert 1 == User.objects.count()

    @pytest.mark.django_db
    def test_user_create_sets_up_default_parameters(self) -> None:
        UserService.user_create(email="example@domain.com", password="password")

        user = User.objects.first()

        assert not user.is_admin
        assert user.is_active

    @pytest.mark.django_db
    def test_user_create_sets_up_custom_parameters(self) -> None:
        UserService.user_create(
            email="example@domain.com",
            password="password",
            is_admin=True,
            is_active=False,
        )

        user = User.objects.first()

        assert user.is_admin
        assert not user.is_active

    @pytest.mark.django_db
    def test_user_create_triggers_email_duplicate_error(self) -> None:
        email = "example@domain.com"
        UserFactory(email=email)

        with pytest.raises(ValidationError):
            UserService.user_create(email=email, password="password")
