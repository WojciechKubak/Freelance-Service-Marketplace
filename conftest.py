from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory
from typing import Callable, Generator, Any
from unittest.mock import Mock, patch
import pytest


@pytest.fixture(scope="session")
def auth_request() -> (
    Callable[[User, str, str, dict[str, Any] | None], APIRequestFactory]
):
    def _make_request(
        user: User, method: str, url: str, data: dict[str, Any] | None = None
    ) -> APIRequestFactory:
        refresh = RefreshToken.for_user(user)
        factory = APIRequestFactory()
        request = getattr(factory, method.lower())(
            url, data, HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        return request

    return _make_request


@pytest.fixture(scope="function", autouse=True)
def mock_create_meeting() -> Generator[Mock, None, None]:
    with patch("apps.consultations.services.create_meeting") as mock:
        instance = mock.return_value
        instance.join_url = "https://example.com/join"
        yield mock
