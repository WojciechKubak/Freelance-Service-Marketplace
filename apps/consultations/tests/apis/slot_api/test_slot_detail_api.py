from apps.consultations.tests.factories import SlotFactory
from apps.consultations.apis.slot_api import SlotDetailApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestSlotDetailApi:

    @pytest.mark.django_db
    def test_api_response_on_not_found_slot(self) -> None:
        request = APIRequestFactory().get("/api/consultations/slots/999/")

        response = SlotDetailApi.as_view()(request, slot_id=999)

        assert 404 == response.status_code

    @pytest.mark.django_db
    def test_api_response_on_success(self) -> None:
        slot = SlotFactory()
        request = APIRequestFactory().get(f"/api/consultations/slots/{slot.id}/")

        response = SlotDetailApi.as_view()(request, slot_id=slot.id)

        expected_response_data = OrderedDict(
            {
                "id": slot.id,
                "start_time": slot.start_time.isoformat().replace("+00:00", "Z"),
                "end_time": slot.end_time.isoformat().replace("+00:00", "Z"),
                "consultation": OrderedDict(
                    {
                        "id": slot.consultation.id,
                        "title": slot.consultation.title,
                        "price": float(slot.consultation.price),
                        "tags": [
                            OrderedDict({"id": tag.id, "name": tag.name})
                            for tag in slot.consultation.tags.all()
                        ],
                    }
                ),
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
