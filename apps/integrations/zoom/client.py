from apps.core.exceptions import ZoomError
from apps.common.utils import assert_settings
from dataclasses import dataclass, fields
from functools import lru_cache
from datetime import datetime
from typing import Any, Self
import httpx
import base64
import json


@dataclass
class ZoomCredentials:
    account_id: str
    client_id: str
    client_secret: str


@dataclass
class MeetingDetails:
    uuid: str
    id: int
    host_id: str
    host_email: str
    topic: str
    type: int
    status: str
    start_time: str
    duration: int
    timezone: str
    created_at: str
    start_url: str
    join_url: str
    password: str
    h323_password: str
    pstn_password: str
    encrypted_password: str
    # settings: Settings
    pre_schedule: bool

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Self:
        # Response is more complex than this, but we only care about these fields
        return cls(
            **{
                k: v
                for k, v in data.items()
                if k in {f.name for f in fields(MeetingDetails)}
            }
        )


@lru_cache
def get_credentials() -> ZoomCredentials:
    settings = assert_settings(
        ["ZOOM_ACCOUNT_ID", "ZOOM_CLIENT_ID", "ZOOM_CLIENT_SECRET"]
    )
    return ZoomCredentials(
        account_id=settings["ZOOM_ACCOUNT_ID"],
        client_id=settings["ZOOM_CLIENT_ID"],
        client_secret=settings["ZOOM_CLIENT_SECRET"],
    )


# https://developers.zoom.us/docs/internal-apps/s2s-oauth/
def _get_oauth_token() -> str:
    zoom_credentials = get_credentials()

    credentials = f"{zoom_credentials.client_id}:{zoom_credentials.client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://zoom.us/oauth/token"

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "account_credentials",
        "account_id": zoom_credentials.account_id,
    }

    response = httpx.post(url, headers=headers, data=data)

    if not str(response.status_code).startswith("2"):
        raise ZoomError("Failed to get OAuth token")

    return response.json()["access_token"]


# https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate
def create_meeting(topic: str, start_time: datetime, duration: int) -> MeetingDetails:
    access_token = _get_oauth_token()

    url = "https://api.zoom.us/v2/users/me/meetings"

    meeting_details = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration": duration,
        "timezone": "UTC",
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = httpx.post(url, headers=headers, data=json.dumps(meeting_details))

    if not str(response.status_code).startswith("2"):
        raise ZoomError("Failed to create meeting")

    return MeetingDetails.from_response(response.json())
