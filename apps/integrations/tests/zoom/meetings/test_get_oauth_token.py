from apps.integrations.zoom.meetings import ZoomError, _get_oauth_token
from unittest.mock import MagicMock, Mock, patch
from typing import Generator
import pytest
import base64


@pytest.fixture(scope="session", autouse=True)
def mock_get_credentials() -> Generator[Mock, None, None]:
    with patch("apps.integrations.zoom.meetings.get_credentials") as mock:
        yield mock


@pytest.fixture(scope="session", autouse=True)
def mock_post() -> Generator[Mock, None, None]:
    with patch("httpx.post") as mock:
        yield mock


def test_get_oauth_token_success(mock_get_credentials, mock_post) -> None:
    mock_credentials = MagicMock()
    mock_credentials.client_id = "fake_client_id"
    mock_credentials.client_secret = "fake_client_secret"
    mock_credentials.account_id = "fake_account_id"
    mock_get_credentials.return_value = mock_credentials

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "fake_access_token"}
    mock_post.return_value = mock_response

    encoded_credentials = base64.b64encode(
        f"{mock_credentials.client_id}:{mock_credentials.client_secret}".encode()
    ).decode()

    token = _get_oauth_token()

    mock_post.assert_called_once_with(
        "https://zoom.us/oauth/token",
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "account_credentials",
            "account_id": mock_credentials.account_id,
        },
    )
    assert "fake_access_token" == token


def test_get_oauth_token_failure(mock_get_credentials, mock_post) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    with pytest.raises(ZoomError, match="Failed to get OAuth token"):
        _get_oauth_token()
