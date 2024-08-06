from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.apis import ConsultationChangeVisibilityApi
from apps.users.tests.factories import UserFactory, User
from rest_framework.test import APIRequestFactory
from typing import Any, Callable
import pytest


class TestConsultationChangeVisibilityApi:

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_unauthorized_user(self) -> None:
        consultation = ConsultationFactory()
        factory = APIRequestFactory()

        request = factory.patch(
            f"/api/consultations/{consultation.id}/visibility", {"is_visible": True}
        )
        response = ConsultationChangeVisibilityApi.as_view()(request, consultation.id)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_required_instance_owner(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory()
        request = auth_request(
            UserFactory(is_active=True),
            "PATCH",
            f"/api/consultations/{consultation.id}/visibility",
            {"is_visible": True},
        )

        response = ConsultationChangeVisibilityApi.as_view()(request, consultation.id)

        expected_response_data = {
            "detail": "You do not have permission to perform this action."
        }

        assert 403 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successfull_visible_change(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory()
        request = auth_request(
            consultation.created_by,
            "PATCH",
            f"/api/consultations/{consultation.id}/visibility",
            {"is_visible": True},
        )

        response = ConsultationChangeVisibilityApi.as_view()(request, consultation.id)

        assert 204 == response.status_code
