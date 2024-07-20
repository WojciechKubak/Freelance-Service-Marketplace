from apps.emails.services import EmailService
from apps.emails.models import Email
from apps.core.exceptions import EmailError
from smtplib import SMTPException
from unittest.mock import patch
import pytest


class TestEmailSend:

    def test_email_status_is_not_ready(self) -> None:
        email = Email(
            to="user@example.com",
            subject="Subject",
            html="html",
            plain_text="text",
            status=Email.Status.SENT,
        )

        with pytest.raises(EmailError):
            EmailService.email_send(email)

    @pytest.mark.django_db
    @patch("apps.emails.services.EmailMultiAlternatives.send")
    def test_email_send_raises_smtp_exception_email_status_changes(
        self, mock_send
    ) -> None:
        mock_send.side_effect = SMTPException

        email = Email(
            to="user@example.com",
            subject="Subject",
            html="html",
            plain_text="text",
        )

        EmailService.email_send(email)

        assert Email.Status.FAILED == Email.objects.first().status

    @pytest.mark.django_db
    @patch("django.core.mail.message.EmailMultiAlternatives.send")
    def test_email_send_correctly_sends_email(self, mock_send) -> None:
        email = Email(
            to="user@example.com",
            subject="Subject",
            html="html",
            plain_text="text",
        )

        EmailService.email_send(email)

        mock_send.assert_called_once()

        assert Email.Status.SENT == Email.objects.first().status
