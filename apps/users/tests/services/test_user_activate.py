from apps.users.tests.factories import UserFactory
from apps.users.models import User
from apps.users.services import UserService
from apps.users.utils import sign_user_id
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import uuid
import pytest


class TestUserActivate:

    def test_user_activate_raises_signature_expired(self, monkeypatch) -> None:
        monkeypatch.setattr(UserService, "EMAIL_TIMEOUT", 0)

        value = sign_user_id("user_id")

        with pytest.raises(ValidationError):
            UserService.user_activate(signed_id=value)

    def test_user_activate_raises_bad_signature(self) -> None:
        value = sign_user_id("user_id")[:-1]

        with pytest.raises(ValidationError):
            UserService.user_activate(signed_id=value)

    @pytest.mark.django_db
    def test_user_activate_raises_object_does_not_exist(self) -> None:
        value = sign_user_id(uuid.uuid4())

        with pytest.raises(ObjectDoesNotExist):
            UserService.user_activate(signed_id=value)

    @pytest.mark.django_db
    def test_user_activate_correctly_activates_user(self) -> None:
        user = UserFactory(is_active=False)
        value = sign_user_id(str(user.id))

        UserService.user_activate(signed_id=value)

        assert User.objects.filter(is_active=True).exists()
