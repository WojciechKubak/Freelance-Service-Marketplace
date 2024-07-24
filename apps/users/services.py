from apps.users.utils import unsign_data, url_generate
from apps.users.models import User
from apps.emails.services import EmailService
from django.core.exceptions import ValidationError
from dataclasses import dataclass
from django.conf import settings


@dataclass
class UserEmailService:

    @staticmethod
    def user_activation_email_send(*, email: str) -> User:
        user = User.objects.get(email=email)

        if user.is_active:
            raise ValidationError("User is already active")

        url = url_generate(user_id=user.id, viewname="activate")
        email = EmailService.send_activation_email(user_email=user.email, url=url)

        return user

    @staticmethod
    def user_reset_password_email_send(*, email: str) -> str:
        user = User.objects.filter(email=email).first()

        if not user or not user.is_active:
            return email

        # todo: service layer tight coupled with view cause of viewname
        url = url_generate(user_id=user.id, viewname="password-reset")
        email = EmailService.send_password_reset_email(user_email=user.email, url=url)

        return user.email


@dataclass
class UserService:

    @staticmethod
    def user_create(
        *,
        email: str,
        password: str,
        is_admin: bool = False,
        is_superuser: bool = False,
    ) -> User:
        if is_superuser:
            user = User.objects.create_superuser(email=email, password=password)
        else:
            user = User.objects.create_user(
                email=email, password=password, is_admin=is_admin
            )

        url = url_generate(user_id=user.id, viewname="activate")
        email = EmailService.send_activation_email(user_email=user.email, url=url)

        return user

    @staticmethod
    def user_activate(*, signed_id: str) -> User:
        user_id = unsign_data(signed_id, max_age=settings.EMAIL_ACTIVATION_TIMEOUT)
        if not user_id:
            raise ValidationError("Activation url is invalid")

        user = User.objects.get(id=user_id)

        user.is_active = True
        user.full_clean()
        user.save()

        return user

    @staticmethod
    def user_reset_password(*, signed_id: str, password: str) -> User:
        user_id = unsign_data(signed_id, max_age=settings.EMAIL_ACTIVATION_TIMEOUT)
        if not user_id:
            raise ValidationError("Invalid value for password reset")

        user = User.objects.get(id=user_id)
        if not user.is_active:
            raise ValidationError("User is not active")

        user.set_password(password)
        user.full_clean()
        user.save()

        return user
