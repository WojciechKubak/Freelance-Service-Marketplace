from apps.emails.services import EmailService
from apps.emails.models import Email
from apps.emails.templates import EmailType
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def email_prepared_mock():
    with patch("apps.emails.services.EmailService._email_prepare") as mock:
        yield mock


@pytest.fixture
def email_send_mock():
    with patch("apps.emails.services.EmailService.email_send") as mock:
        yield mock


class TestSendActivationEmail:

    @pytest.mark.django_db
    def test_send_activation_email(self, email_prepared_mock, email_send_mock) -> None:
        user_email = "user@example.com"
        url = "http://example.com/activate"
        prepared_email = MagicMock(spec=Email)
        email_send_mock.return_value = prepared_email

        result = EmailService.send_activation_email(user_email=user_email, url=url)

        email_prepared_mock.assert_called_once_with(
            user_email=user_email, email_type=EmailType.ACTIVATION, context={"url": url}
        )

        assert prepared_email == result
