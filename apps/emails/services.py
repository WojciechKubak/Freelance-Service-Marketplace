from apps.core.exceptions import EmailError
from apps.emails.models import Email
from apps.emails.templates import EmailType
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from dataclasses import dataclass
from smtplib import SMTPException


@dataclass
class EmailService:

    @staticmethod
    def send_activation_email(user_email: str, url: str) -> Email:
        prepared = EmailService._email_prepare(
            user_email=user_email,
            email_type=EmailType.ACTIVATION,
            context={"url": url},
        )
        email = EmailService.email_send(prepared)

        return email

    @staticmethod
    def send_password_reset_email(user_email: str, url: str) -> Email:
        prepared = EmailService._email_prepare(
            user_email=user_email,
            email_type=EmailType.PASSWORD_RESET,
            context={"url": url},
        )
        email = EmailService.email_send(prepared)

        return email

    @staticmethod
    def email_send(email: Email) -> Email:
        if email.status != Email.Status.READY:
            raise EmailError("Email is not ready to be sent")

        msg = EmailMultiAlternatives(
            subject=email.subject,
            body=email.plain_text,
            to=[email.to],
        )

        if hasattr(email, "html") and email.html:
            msg.attach_alternative(email.html, "text/html")

        try:
            msg.send()
            email.sent_at = timezone.now()
            email.status = Email.Status.SENT

        except SMTPException:
            email.status = Email.Status.FAILED

        email.full_clean()
        email.save()

        return email

    @staticmethod
    def _email_prepare(
        *, user_email: str, email_type: EmailType, context: dict[str, str]
    ) -> Email:
        template = email_type.value()

        html = render_to_string(template.html_path, context)
        plain = render_to_string(template.plain_text_path, context)

        email = Email(
            to=user_email,
            subject=template.subject,
            html=html,
            plain_text=plain,
        )

        email.full_clean()
        email.save()

        return email
