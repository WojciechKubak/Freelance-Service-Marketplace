from apps.emails.services import EmailService
from apps.emails.models import Email
from apps.emails.templates import EmailType
from unittest.mock import patch, MagicMock
from typing import Generator
import pytest


@pytest.fixture
def email_prepared_mock() -> Generator[MagicMock, None, None]:
    with patch("apps.emails.services.EmailService._email_prepare") as mock:
        yield mock


@pytest.fixture
def email_send_mock() -> Generator[MagicMock, None, None]:
    with patch("apps.emails.services.EmailService.email_send") as mock:
        yield mock


@pytest.mark.django_db
def test_send_password_reset_email_on_success(
    email_prepared_mock: Generator[MagicMock, None, None],
    email_send_mock: Generator[MagicMock, None, None],
) -> None:
    user_email = "user@example.com"
    url = "http://example.com/reset"

    prepared_email = MagicMock(spec=Email)
    email_send_mock.return_value = prepared_email

    result = EmailService.send_password_reset_email(user_email=user_email, url=url)

    email_prepared_mock.assert_called_once_with(
        user_email=user_email,
        email_type=EmailType.PASSWORD_RESET,
        context={"url": url},
    )
    assert prepared_email == result
