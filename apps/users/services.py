from apps.users.models import User
from apps.emails.services import EmailService
from django.core.signing import TimestampSigner
from django.core.exceptions import ValidationError
from dataclasses import dataclass
from django.urls import reverse
from django.conf import settings


@dataclass
class UserEmailService:

    @staticmethod
    def user_activation_email_send(*, email: str) -> User:
        user = User.objects.get(email=email)

        if user.is_active:
            raise ValidationError("User is already active")

        link = UserEmailService._url_create(user_id=user.id, viewname="activate")
        email = EmailService.send_activation_email(user_email=user.email, url=link)

        return user

    @staticmethod
    def _url_create(*, user_id: str, viewname: str) -> str:
        signer = TimestampSigner()
        signed_id = signer.sign(user_id)

        url = reverse(viewname, kwargs={"user_id": signed_id})

        return f"{settings.BASE_BACKEND_URL}{url}"


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

        link = UserEmailService._url_create(user_id=user.id, viewname="activate")
        email = EmailService.send_activation_email(user_email=user.email, url=link)

        return user

    @staticmethod
    def user_activate(*, signed_value: str) -> User:
        signer = TimestampSigner()
        unsigned_id = signer.unsign(
            signed_value, max_age=settings.EMAIL_ACTIVATION_TIMEOUT
        )

        user = User.objects.get(id=unsigned_id)

        user.is_active = True
        user.save()

        return user
