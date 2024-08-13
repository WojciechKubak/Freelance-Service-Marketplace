from apps.users.tests.factories import UserFactory, User
from apps.categorization.tests.factories import TagFactory
from apps.consultations.apis.consultation_api import ConsultationCreateApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any
import pytest


class TestConsultationCreateApi:
    simple_field_data: dict[str, str] = {
        "title": "Consultation 1",
        "description": "Description 1",
        "price": 999.0,
    }

    @pytest.mark.django_db
    def test_api_response_on_non_existing_tag(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        request = auth_request(
            UserFactory(),
            "POST",
            "api/consultations/create",
            self.simple_field_data | {"tags": [999]},
        )

        response = ConsultationCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": ["One or more tags do not exist."]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_success(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        tags = TagFactory.create_batch(3)
        request = auth_request(
            UserFactory(),
            "POST",
            "api/consultations/create",
            self.simple_field_data | {"tags": [tag.id for tag in tags]},
        )

        response = ConsultationCreateApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "id": 1,
                **self.simple_field_data,
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

        assert 201 == response.status_code
        assert expected_response_data == response.data
