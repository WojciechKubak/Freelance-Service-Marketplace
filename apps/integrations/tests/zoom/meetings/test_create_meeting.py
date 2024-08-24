from apps.integrations.zoom.meetings import ZoomError, create_meeting
from django.utils import timezone
from unittest.mock import Mock, MagicMock, patch
from typing import Generator
import pytest
import json


@pytest.fixture(scope="session", autouse=True)
def mock_get_oauth_token() -> Generator[Mock, None, None]:
    with patch("apps.integrations.zoom.meetings._get_oauth_token") as mock:
        mock.return_value = "fake_access_token"
        yield mock


@pytest.fixture(scope="session", autouse=True)
def mock_post() -> Generator[Mock, None, None]:
    with patch("httpx.post") as mock:
        yield mock


@patch("apps.integrations.zoom.meetings.MeetingDetails.from_response")
def test_create_meeting_success(mock_from_response, mock_post) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "123456789",
        "join_url": "https://example.com/join",
    }
    mock_post.return_value = mock_response

    mock_meeting_details = MagicMock()
    mock_meeting_details.id = "123456789"
    mock_meeting_details.join_url = "https://example.com/join"
    mock_from_response.return_value = mock_meeting_details

    url = "https://api.zoom.us/v2/users/me/meetings"
    topic = "Test Meeting"
    start_time = timezone.now()
    duration = 60

    result = create_meeting(topic, start_time, duration)

    mock_post.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer fake_access_token",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "topic": topic,
                "type": 2,
                "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "duration": duration,
                "timezone": "UTC",
            }
        ),
    )
    assert result.id == "123456789"
    assert result.join_url == "https://example.com/join"


def test_create_meeting_failure(mock_post) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    with pytest.raises(ZoomError, match="Failed to create meeting"):
        create_meeting("Test Meeting", timezone.now(), 60)
