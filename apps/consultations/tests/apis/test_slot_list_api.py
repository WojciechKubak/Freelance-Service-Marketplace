from apps.consultations.tests.factories import SlotFactory, ConsultationFactory
from apps.consultations.apis import SlotListApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


@pytest.mark.django_db
def test_api_response_on_listed_slots() -> None:
    consultation = ConsultationFactory()
    slots = SlotFactory.create_batch(2, consultation=consultation)

    request = APIRequestFactory().get(
        f"/api/consultations/slots/?consultation_id={consultation.id}"
    )

    response = SlotListApi.as_view()(request)

    expected_response_data = OrderedDict(
        {
            "count": len(slots),
            "next": None,
            "previous": None,
            "results": [
                OrderedDict(
                    {
                        "id": slot.id,
                        "start_time": slot.start_time.isoformat().replace(
                            "+00:00", "Z"
                        ),
                        "end_time": slot.end_time.isoformat().replace("+00:00", "Z"),
                    }
                )
                for slot in slots
            ],
        }
    )

    assert 200 == response.status_code
    assert expected_response_data == response.data
