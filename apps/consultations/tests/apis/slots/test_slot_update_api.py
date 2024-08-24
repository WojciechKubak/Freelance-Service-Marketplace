from apps.users.tests.factories import UserFactory
from apps.consultations.tests.factories import SlotFactory
from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.apis.slots import SlotUpdateApi
from apps.consultations.services.slots import (
    SLOT_VALIDATE_MINIMAL_DURATION_TIME,
    SLOT_VALIDATE_CONSULTATION_VISIBILITY,
    SLOT_VALIDATE_OVERLAP,
    SlotService,
)
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestSlotUpdateApi:
    simple_field_data: dict[str, str] = {
        "start_time": "2021-01-01T00:00:00Z",
        "end_time": "2021-01-01T01:00:00Z",
    }

    def test_api_response_on_slot_not_found(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        request = auth_request(
            UserFactory(),
            "PUT",
            "/api/consultations/slots/999/update/",
            self.simple_field_data,
        )

        response = SlotUpdateApi.as_view()(request, 999)

        assert 404 == response.status_code

    def test_api_response_on_duration_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        slot = SlotFactory()
        request = auth_request(
            slot.consultation.created_by,
            "PUT",
            f"/api/consultations/slots/{slot.id}/update/",
            {
                "start_time": "2021-01-01T00:00:00Z",
                "end_time": "2021-01-01T00:30:00Z",
            },
        )

        response = SlotUpdateApi.as_view()(request, slot.id)

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

    def test_api_response_on_slot_overlap_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        pass
        consultation = ConsultationFactory()
        slot1, slot2 = SlotFactory.create_batch(2, consultation=consultation)

        request = auth_request(
            consultation.created_by,
            "PUT",
            f"/api/consultations/slots/{slot1.id}/update/",
            {
                "consultation_id": consultation.id,
                "start_time": slot2.start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end_time": slot2.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        )

        response = SlotUpdateApi.as_view()(request, slot1.id)

        expected_response_data = {
            "detail": {"non_field_errors": [SLOT_VALIDATE_OVERLAP]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_consultation_visibility_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        consultation = ConsultationFactory(is_visible=False)
        slot = SlotFactory(consultation=consultation)

        request = auth_request(
            slot.consultation.created_by,
            "PUT",
            f"/api/consultations/slots/{slot.id}/update/",
            {"consultation_id": consultation.id, **self.simple_field_data},
        )

        response = SlotUpdateApi.as_view()(request, slot.id)

        expected_response_data = {
            "detail": {"non_field_errors": [SLOT_VALIDATE_CONSULTATION_VISIBILITY]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_slot_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        slot = SlotFactory()

        request = auth_request(
            slot.consultation.created_by,
            "PUT",
            f"/api/consultations/slots/{slot.id}/update/",
            {
                "id": slot.id,
                **self.simple_field_data,
            },
        )

        response = SlotUpdateApi.as_view()(request, slot.id)

        expected_response_data = OrderedDict({"id": 1, **self.simple_field_data})

        assert 200 == response.status_code
        assert expected_response_data == response.data
