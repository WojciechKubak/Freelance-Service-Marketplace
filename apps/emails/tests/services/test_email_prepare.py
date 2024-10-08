from apps.users.tests.factories import UserFactory
from apps.emails.services import _email_prepare
from apps.emails.templates import EmailType
from apps.emails.models import Email
from django.template.loader import render_to_string
import pytest


@pytest.mark.django_db
def test_email_prepare_correctly_creates_email_instance() -> None:
    user = UserFactory()
    context = {"url": "http://example.com/example"}

    result = _email_prepare(
        user_email=user.email, email_type=EmailType.ACTIVATION, context=context
    )

    assert Email.objects.first() == result
    assert user.email == result.to

    template = EmailType.ACTIVATION.value()

    expected_html = render_to_string(template.html_path, context)
    expected_plain_text = render_to_string(template.plain_text_path, context)

    assert template.subject == result.subject
    assert expected_html == result.html
    assert expected_plain_text == result.plain_text
