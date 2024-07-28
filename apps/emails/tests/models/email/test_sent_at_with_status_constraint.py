from apps.emails.models import Email
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_email_sent_at_cannot_be_null_for_sent_email_constraint() -> None:
    with pytest.raises(ValidationError):
        email = Email(
            to="user@example.com",
            subject="test mail",
            html="content",
            plain_text="content",
            status=Email.Status.READY,
            sent_at=timezone.now(),
        )

        email.full_clean()
        email.save()
