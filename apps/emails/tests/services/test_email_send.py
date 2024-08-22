from apps.emails.tests.factories import EmailFactory
from apps.emails.services import email_send
from apps.emails.models import Email
from apps.core.exceptions import EmailError
from smtplib import SMTPException
from unittest.mock import patch
import pytest


class TestEmailSend:

    @pytest.mark.django_db
    def test_email_status_is_not_ready(self) -> None:
        with pytest.raises(EmailError):
            email = EmailFactory(status=Email.Status.SENT)
            email_send(email=email)

    @pytest.mark.django_db
    @patch("apps.emails.services.EmailMultiAlternatives.send")
    def test_email_send_raises_smtp_exception_email_status_changes(
        self, mock_send
    ) -> None:
        mock_send.side_effect = SMTPException

        email = EmailFactory()

        email_send(email=email)

        assert Email.Status.FAILED == Email.objects.first().status

    @pytest.mark.django_db
    @patch("django.core.mail.message.EmailMultiAlternatives.send")
    def test_email_send_correctly_sends_email(self, mock_send) -> None:
        email = EmailFactory()

        email_send(email=email)

        mock_send.assert_called_once()
        assert Email.Status.SENT == Email.objects.first().status
