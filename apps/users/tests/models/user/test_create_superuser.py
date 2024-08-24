from apps.users.tests.factories import UserFactory
from apps.users.models import User
from django.core.exceptions import ValidationError
import pytest


class TestCreateSuperUser:

    def test_create_superuser_creates_user_instance_in_database(self) -> None:
        User.objects.create_superuser(email="example@domain.com")
        assert 1 == User.objects.count()

    def test_creating_user_with_existing_email_raises_error(self) -> None:
        email = "example@domain.com"

        UserFactory(email=email)

        with pytest.raises(ValidationError):
            User.objects.create_superuser(email=email)

        assert 1 == User.objects.count()

    def test_create_superuser_sets_up_expected_auth_fields(self) -> None:
        User.objects.create_superuser(email="example@domain.com")

        user = User.objects.first()

        assert user.is_admin is True
        assert user.is_active is True

    def test_superuser_without_password_is_created_with_unusable_one(self) -> None:
        user = User.objects.create_superuser(email="example@domain.com")
        assert not user.has_usable_password()
