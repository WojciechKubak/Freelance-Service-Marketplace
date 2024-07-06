from apps.api.apis import HealthCheckAPI
from rest_framework.test import APIRequestFactory


def test_health_check_api_returns_expected_response_status_code_and_data() -> None:
    factory = APIRequestFactory()
    request = factory.get("health/")

    response = HealthCheckAPI.as_view()(request)

    assert 200 == response.status_code
    assert {"message": "Healthy"} == response.data
