from apps.users.utils import sign_data, unsign_data
from apps.users.models import User
from apps.emails.services import EmailService
from django.core.exceptions import ValidationError
from dataclasses import dataclass
from django.conf import settings
from django.urls import reverse


@dataclass
class UserService:
    ACTIVATION_VIEWNAME: str = "activate"
    PASSWORD_RESET_VIEWNAME: str = "password-reset"

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

    @staticmethod
    def user_password_change(
        *, user: User, password: str, new_password: str, new_password_confirm: str
    ) -> User:
        if not user.check_password(password):
            raise ValidationError("Invalid password")

        if new_password != new_password_confirm:
            raise ValidationError("Passwords do not match")

        user.set_password(new_password)
        user.full_clean()
        user.save()

        return user

    @staticmethod
    def _url_generate(*, user_id: str, viewname: str) -> str:
        signed_id = sign_data(user_id)
        url = reverse(viewname, args=[signed_id])
        return f"{settings.BASE_BACKEND_URL}{url}"

    def user_create(
        self,
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

        url = self._url_generate(user_id=user.id, viewname=self.ACTIVATION_VIEWNAME)
        email = EmailService.send_activation_email(user_email=user.email, url=url)

        return user

    def user_activation_email_send(self, *, email: str) -> User:
        user = User.objects.get(email=email)

        if user.is_active:
            raise ValidationError("User is already active")

        url = self._url_generate(user_id=user.id, viewname=self.ACTIVATION_VIEWNAME)
        email = EmailService.send_activation_email(user_email=user.email, url=url)

        return user

    def user_reset_password_email_send(self, *, email: str) -> str:
        user = User.objects.filter(email=email).first()

        if not user or not user.is_active:
            return email

        url = self._url_generate(user_id=user.id, viewname=self.PASSWORD_RESET_VIEWNAME)
        email = EmailService.send_password_reset_email(user_email=user.email, url=url)

        return user.email
