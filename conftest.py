from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory
from typing import Callable, Generator, Any
from unittest.mock import Mock, patch
import pytest


# https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-give-database-access-to-all-my-tests-without-the-django-db-marker
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db) -> None:
    pass


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
    with patch("apps.consultations.services.bookings.create_meeting") as mock:
        instance = mock.return_value
        instance.join_url = "https://example.com/join"
        yield mock


@pytest.fixture(scope="function", autouse=True)
def mock_text_to_file_local_upload() -> Generator[Mock, None, None]:
    with patch(
        "apps.consultations.services.consultations.text_to_file_local_upload"
    ) as mock:
        mock.return_value = None
        yield mock


@pytest.fixture(scope="function", autouse=True)
def mock_local_file_get_content() -> Generator[Mock, None, None]:
    with patch(
        "apps.consultations.selectors.consultations.local_file_get_content"
    ) as mock:
        mock.return_value = "content"
        yield mock
