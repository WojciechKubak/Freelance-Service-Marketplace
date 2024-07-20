from apps.users.models import User
from apps.emails.services import EmailService, EmailType
from django.core.signing import TimestampSigner
from dataclasses import dataclass
from django.urls import reverse
from django.conf import settings


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

        link = UserService._activation_link_create(user_id=user.id)

        email = EmailService.email_prepare(
            user_email=user.email,
            email_type=EmailType.ACTIVATION,
            context={"activation_link": link},
        )
        EmailService.email_send(email)

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

    @staticmethod
    def _activation_link_create(*, user_id: str) -> str:
        signer = TimestampSigner()
        signed_id = signer.sign(user_id)

        activation_url = reverse("activate", kwargs={"user_id": signed_id})

        return f"{settings.BASE_BACKEND_URL}{activation_url}"
