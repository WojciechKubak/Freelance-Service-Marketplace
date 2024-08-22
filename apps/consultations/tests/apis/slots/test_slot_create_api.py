from apps.consultations.tests.factories import SlotFactory
from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.apis.slots import SlotCreateApi
from apps.consultations.services.slots import (
    SLOT_VALIDATE_CONSULTATION_VISIBILITY,
    SLOT_VALIDATE_MINIMAL_DURATION_TIME,
    SLOT_VALIDATE_OVERLAP,
    SlotService,
)
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any
import pytest


class TestSlotCreateApi:
    url: str = "/api/consultations/slots/"
    simple_field_data: dict[str, str] = {
        "start_time": "2021-01-01T00:00:00Z",
        "end_time": "2021-01-01T01:00:00Z",
    }

    @pytest.mark.django_db
    def test_api_response_raises_on_duration_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory()
        request = auth_request(
            consultation.created_by,
            "POST",
            self.url,
            {
                "consultation_id": consultation.id,
                "start_time": "2021-01-01T00:00:00Z",
                "end_time": "2021-01-01T00:30:00Z",
            },
        )

        response = SlotCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {
                "non_field_errors": [
                    SLOT_VALIDATE_MINIMAL_DURATION_TIME.format(
                        SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES
                    )
                ]
            }
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_slot_overlap_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        pass
        slot = SlotFactory()

        request = auth_request(
            slot.consultation.created_by,
            "POST",
            self.url,
            {
                "consultation_id": slot.consultation.id,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
            },
        )

        response = SlotCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": [SLOT_VALIDATE_OVERLAP]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_consultation_visibility_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory(is_visible=False)

        request = auth_request(
            consultation.created_by,
            "POST",
            self.url,
            {"consultation_id": consultation.id, **self.simple_field_data},
        )

        response = SlotCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": [SLOT_VALIDATE_CONSULTATION_VISIBILITY]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successful_slot_creation(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory(is_visible=True)

        request = auth_request(
            consultation.created_by,
            "POST",
            self.url,
            {
                "consultation_id": consultation.id,
                **self.simple_field_data,
            },
        )

        response = SlotCreateApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "id": 1,
                **self.simple_field_data,
                "consultation": {
                    "id": consultation.id,
                    "title": consultation.title,
                    "price": float(consultation.price),
                    "tags": [
                        {"id": tag.id, "name": tag.name}
                        for tag in consultation.tags.all()
                    ],
                },
            }
        )

        assert 201 == response.status_code
        assert expected_response_data == response.data
