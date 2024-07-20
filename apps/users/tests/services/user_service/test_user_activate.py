from apps.users.tests.factories import UserFactory
from apps.users.models import User
from apps.users.services import UserService
from django.core.signing import SignatureExpired, BadSignature
from django.core.signing import TimestampSigner
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import uuid
import pytest


def sign_value(value: str) -> str:
    signer = TimestampSigner()
    return signer.sign(value)


class TestUserActivate:

    def test_user_activate_raises_signature_expired(self, monkeypatch) -> None:
        monkeypatch.setattr(settings, "EMAIL_ACTIVATION_TIMEOUT", 0)

        value = sign_value("user_id")

        with pytest.raises(SignatureExpired):
            UserService.user_activate(signed_value=value)

    def test_user_activate_raises_bad_signature(self) -> None:
        value = sign_value("user_id")[:-1]

        with pytest.raises(BadSignature):
            UserService.user_activate(signed_value=value)

    @pytest.mark.django_db
    def test_user_activate_raises_object_does_not_exist(self) -> None:
        value = sign_value(uuid.uuid4())

        with pytest.raises(ObjectDoesNotExist):
            UserService.user_activate(signed_value=value)

    @pytest.mark.django_db
    def test_user_activate_correctly_activates_user(self) -> None:
        user = UserFactory(is_active=False)
        value = sign_value(str(user.id))

        UserService.user_activate(signed_value=value)

        assert User.objects.filter(is_active=True).exists()
