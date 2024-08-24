from apps.consultations.tests.factories import ConsultationFactory
from apps.categorization.tests.factories import TagFactory
from apps.users.tests.factories import UserFactory, User
from apps.consultations.apis.consultations import ConsultationUpdateApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any
from decimal import Decimal


class TestConsultationUpdateApi:
    simple_field_data: dict[str, str] = {
        "title": "Consultation 1",
        "content": "content 1",
        "price": Decimal("999.0"),
    }

    def test_api_response_on_unauthorized_user(self) -> None:
        consultation = ConsultationFactory()

        factory = APIRequestFactory()
        request = factory.post(
            f"api/consultations/{consultation.id}/update",
            self.simple_field_data,
        )

        response = ConsultationUpdateApi.as_view()(request, consultation.id)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_invalid_consultation_id(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)

        request = auth_request(
            user,
            "POST",
            "api/consultations/999/update",
            self.simple_field_data,
        )

        response = ConsultationUpdateApi.as_view()(request, 999)

        expected_response_data = {"detail": "Not found."}

        assert 404 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_for_user_that_is_not_instance_creator(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        first, second = UserFactory.create_batch(2, is_active=True)
        consultation = ConsultationFactory(created_by=first)

        request = auth_request(
            second,
            "POST",
            f"api/consultations/{consultation.id}/update",
            self.simple_field_data,
        )

        response = ConsultationUpdateApi.as_view()(request, consultation.id)

        expected_response_data = {
            "detail": "You do not have permission to perform this action."
        }

        assert 403 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_missing_all_data_fields(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        consultation = ConsultationFactory(created_by=user)

        request = auth_request(
            user, "POST", f"api/consultations/{consultation.id}/update", {}
        )

        response = ConsultationUpdateApi.as_view()(request, consultation.id)

        expected_response_data = OrderedDict(
            {
                "id": consultation.id,
                "title": consultation.title,
                "price": float(consultation.price),
                "tags": [
                    OrderedDict(
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                    )
                    for tag in consultation.tags.all().order_by("id")
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_simple_fields_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        consultation = ConsultationFactory(created_by=user)

        request = auth_request(
            user,
            "POST",
            f"api/consultations/{consultation.id}/update",
            self.simple_field_data,
        )

        response = ConsultationUpdateApi.as_view()(request, consultation.id)

        expected_response_data = OrderedDict(
            {
                "id": consultation.id,
                "title": self.simple_field_data["title"],
                "price": float(self.simple_field_data["price"]),
                "tags": [
                    OrderedDict(
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                    )
                    for tag in consultation.tags.all().order_by("id")
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_m2m_field_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        consultation = ConsultationFactory(created_by=user)
        tags = TagFactory.create_batch(3)

        request = auth_request(
            user,
            "POST",
            f"api/consultations/{consultation.id}/update",
            {"tags": [tag.id for tag in tags]},
        )

        response = ConsultationUpdateApi.as_view()(request, consultation.id)

        expected_response_data = OrderedDict(
            {
                "id": consultation.id,
                "title": consultation.title,
                "price": float(consultation.price),
                "tags": [
                    OrderedDict(
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                    )
                    for tag in tags
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
