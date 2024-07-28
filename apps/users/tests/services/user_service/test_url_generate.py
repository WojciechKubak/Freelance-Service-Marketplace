from apps.users.services import UserService
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch


@patch("django.core.signing.TimestampSigner.sign")
def test_url_generate_creates_expected_url(mock_sign) -> None:
    mock_sign.return_value = "signed_user_id"
    user_id = "test_user_id"

    result = UserService._url_generate(
        user_id=user_id, viewname="api:users:user-activate"
    )

    endpoint = reverse(
        "api:users:user-activate", kwargs={"signed_id": "signed_user_id"}
    )
    expected = f"{settings.BASE_BACKEND_URL}{endpoint}"

    mock_sign.assert_called_once_with(user_id)
    assert expected == result
