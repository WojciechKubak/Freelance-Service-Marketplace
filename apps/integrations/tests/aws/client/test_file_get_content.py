from apps.integrations.aws.client import AWSS3Error, file_get_content
from botocore.exceptions import BotoCoreError, ClientError
from unittest.mock import MagicMock
import pytest


def test_file_get_content_success(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_response = {"Body": MagicMock(read=MagicMock(return_value=b"test content"))}
    mock_s3.get_object.return_value = mock_response
    mock_boto3_client.return_value = mock_s3

    result = file_get_content(file_name="test_file.txt")

    mock_s3.get_object.assert_called_once_with(
        Bucket="test_bucket_name", Key="test_file.txt"
    )
    assert "test content" == result


def test_file_get_content_failure(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.get_object.side_effect = ClientError({"Error": {}}, "get_object")
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(AWSS3Error, match="Failed to get file test_file.txt"):
        file_get_content(file_name="test_file.txt")


def test_file_get_content_boto_core_error(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.get_object.side_effect = BotoCoreError
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(AWSS3Error, match="Failed to get file test_file.txt"):
        file_get_content(file_name="test_file.txt")
