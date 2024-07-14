from apps.users.tests.factories import UserFactory
from apps.users.models import User
from django.core.exceptions import ValidationError
import pytest


class TestCreateUser:

    @pytest.mark.django_db
    def test_create_user_creates_user_instance_in_database(self) -> None:
        User.objects.create_user(email="example@domain.com")
        assert 1 == User.objects.count()

    @pytest.mark.django_db
    def test_creating_user_with_existing_email_raises_error(self) -> None:
        email = "example@domain.com"

        UserFactory(email=email)

        with pytest.raises(ValidationError):
            User.objects.create_user(email=email)

        assert 1 == User.objects.count()

    @pytest.mark.django_db
    def test_create_user_sets_up_default_parameters(self) -> None:
        User.objects.create_user(email="example@domain.com", password="password")

        user = User.objects.first()

        assert not user.is_admin
        assert user.is_active

    @pytest.mark.django_db
    def test_create_user_normalizes_email_field(self) -> None:
        email = "Example@DOMAIN.com"
        User.objects.create_user(email=email, password="password")

        user = User.objects.first()

        assert user.email == email.lower()

    @pytest.mark.django_db
    def test_user_without_password_is_created_with_unusable_one(self) -> None:
        user = User.objects.create_user(email="example@domain.com", password=None)
        assert not user.has_usable_password()
