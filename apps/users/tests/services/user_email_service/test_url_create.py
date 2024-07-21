from apps.users.services import UserEmailService
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch


@patch("django.core.signing.TimestampSigner.sign")
def test_url_create_generates_expected_url(mock_sign) -> None:
    mock_sign.return_value = "signed_user_id"
    user_id = "test_user_id"

    result = UserEmailService._url_create(user_id=user_id, viewname="activate")

    endpoint = reverse("activate", kwargs={"user_id": "signed_user_id"})
    expected_activation_url = f"{settings.BASE_BACKEND_URL}{endpoint}"

    mock_sign.assert_called_once_with(user_id)
    assert expected_activation_url == result
