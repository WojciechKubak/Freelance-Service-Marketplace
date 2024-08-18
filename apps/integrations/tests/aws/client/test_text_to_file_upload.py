from apps.integrations.aws.client import (
    text_to_file_upload,
    PutObjectResponse,
    AWSS3Error,
)
from botocore.exceptions import BotoCoreError, ClientError
from typing import Any
from unittest.mock import MagicMock
import pytest


@pytest.fixture(scope="session")
def example_response() -> dict[str, Any]:
    return {
        "ResponseMetadata": {
            "RequestId": "test_request_id",
            "HostId": "test_host_id",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-id-2": "test_amz_id_2",
                "x-amz-request-id": "test_request_id",
                "date": "test_date",
                "etag": '"test_etag"',
                "x-amz-server-side-encryption": "AES256",
                "content-type": "text/plain",
                "content-length": "15",
            },
            "RetryAttempts": 0,
        },
        "ETag": '"test_etag"',
        "ServerSideEncryption": "AES256",
    }


def test_text_to_file_upload_success(mock_boto3_client, example_response) -> None:
    mock_s3 = MagicMock()

    mock_s3.put_object.return_value = example_response
    mock_boto3_client.return_value = mock_s3

    result = text_to_file_upload(file_name="test_file.txt", content="test content")

    mock_s3.put_object.assert_called_once_with(
        Bucket="test_bucket_name",
        Key="test_file.txt",
        Body="test content",
        ContentType="text/plain",
    )
    assert PutObjectResponse.from_response(example_response) == result


def test_text_to_file_upload_failure(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.put_object.side_effect = ClientError({"Error": {}}, "put_object")
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(AWSS3Error, match="Failed to upload file test_file.txt"):
        text_to_file_upload(file_name="test_file.txt", content="test content")


def test_text_to_file_upload_boto_core_error(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.put_object.side_effect = BotoCoreError
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(AWSS3Error, match="Failed to upload file test_file.txt"):
        text_to_file_upload(file_name="test_file.txt", content="test content")
