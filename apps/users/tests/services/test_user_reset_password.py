from apps.users.tests.factories import UserFactory
from apps.users.services import (
    USER_PASSWORD_RESET_LINK_INVALID,
    USER_NOT_ACTIVE,
    UserService,
    sign_user_id,
)
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import uuid
import pytest


class TestUserResetPassword:

    def test_password_reset_raises_signature_expired(self, monkeypatch) -> None:
        monkeypatch.setattr(UserService, "EMAIL_TIMEOUT", 0)

        value = sign_user_id("user_id")

        with pytest.raises(ValidationError, match=USER_PASSWORD_RESET_LINK_INVALID):
            UserService.user_reset_password(signed_id=value, password="password")

    def test_password_reset_raises_bad_signature(self) -> None:
        value = sign_user_id("user_id")[:-1]

        with pytest.raises(ValidationError, match=USER_PASSWORD_RESET_LINK_INVALID):
            UserService.user_reset_password(signed_id=value, password="password")

    def test_password_reset_raises_object_does_not_exist(self) -> None:
        value = sign_user_id(str(uuid.uuid4()))

        with pytest.raises(ObjectDoesNotExist):
            UserService.user_reset_password(signed_id=value, password="password")

    def test_password_reset_raises_user_not_active(self) -> None:
        user = UserFactory(is_active=False)
        value = sign_user_id(str(user.id))

        with pytest.raises(ValidationError, match=USER_NOT_ACTIVE):
            UserService.user_reset_password(signed_id=value, password="password")

    def test_password_reset_on_success(self) -> None:
        user = UserFactory(is_active=True)
        value = sign_user_id(str(user.id))

        UserService.user_reset_password(signed_id=value, password="password")

        assert user.check_password("password")
