from apps.users.tests.factories import UserFactory
from apps.users.services import (
    USER_INVALID_PASSWORD,
    USER_INVALID_PASSWORD_CONFIRM,
    UserService,
)
from django.core.exceptions import ValidationError
import pytest


class TestUserPasswordChange:
    password: str = "password"

    @pytest.mark.django_db
    def test_password_reset_on_failed_due_to_incorrect_password(self) -> None:
        user = UserFactory(password=self.password)

        with pytest.raises(ValidationError, match=USER_INVALID_PASSWORD):
            UserService.user_password_change(
                user=user,
                password=f"{self.password}_incorrect",
                new_password="new_password",
                new_password_confirm="new_password",
            )

    @pytest.mark.django_db
    def test_password_reset_on_failed_due_to_incorrect_password_repeat(self) -> None:
        user = UserFactory(password=self.password)

        with pytest.raises(ValidationError, match=USER_INVALID_PASSWORD_CONFIRM):
            UserService.user_password_change(
                user=user,
                password=f"{self.password}",
                new_password="new_password",
                new_password_confirm="new_password_incorrect",
            )

    @pytest.mark.django_db
    def test_user_password_change_succesfully_sets_new_password(self) -> None:
        user = UserFactory(password=self.password)

        new_password = f"new_{self.password}"
        UserService.user_password_change(
            user=user,
            password=self.password,
            new_password=new_password,
            new_password_confirm=new_password,
        )

        assert user.check_password(new_password)
