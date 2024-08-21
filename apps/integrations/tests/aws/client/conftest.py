from apps.integrations.aws.client import S3Credentials
from typing import Generator
from unittest.mock import patch
import pytest


@pytest.fixture
def s3_credentials() -> S3Credentials:
    return S3Credentials(
        access_key_id="test_access_key_id",
        secret_access_key="test_secret_access_key",
        bucket_name="test_bucket_name",
    )


@pytest.fixture(autouse=True)
def patched_s3_get_credentials(s3_credentials) -> Generator:
    with patch(
        "apps.integrations.aws.client.s3_get_credentials", return_value=s3_credentials
    ):
        yield


@pytest.fixture
def mock_boto3_client() -> Generator:
    with patch("apps.integrations.aws.client.boto3.client") as mock_client:
        yield mock_client
