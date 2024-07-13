from apps.users.models import User
from dataclasses import dataclass


@dataclass
class UserService:

    @staticmethod
    def user_create(
        *,
        email: str,
        password: str,
        is_admin: bool = False,
        is_active: bool = True,
    ) -> User:
        user = User.objects.create_user(
            email=email, password=password, is_admin=is_admin, is_active=is_active
        )
        return user
