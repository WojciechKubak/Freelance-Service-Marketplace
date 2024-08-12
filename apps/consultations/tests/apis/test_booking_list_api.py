from apps.consultations.tests.factories import BookingFactory
from apps.users.tests.factories import UserFactory, User
from apps.consultations.apis import BookingListApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Any, Callable
import pytest


@pytest.mark.django_db
def test_api_response_on_bookings_found(
    auth_request: Callable[[User, str, str, dict[str, Any] | None], APIRequestFactory]
) -> None:
    user = UserFactory()
    bookings = BookingFactory.create_batch(2, booked_by=user)

    request = auth_request(user, "GET", "/api/consultations/bookings/")

    response = BookingListApi.as_view()(request)

    expected_response_data = [
        OrderedDict(
            {
                "id": booking.id,
                "start_time": booking.start_time.isoformat().replace("+00:00", "Z"),
                "end_time": booking.end_time.isoformat().replace("+00:00", "Z"),
                "slot": {
                    "id": booking.slot.id,
                    "consultation": {
                        "id": booking.slot.consultation.id,
                        "title": booking.slot.consultation.title,
                        "created_by": {
                            "id": str(booking.slot.consultation.created_by.id),
                            "email": booking.slot.consultation.created_by.email,
                        },
                    },
                },
            }
        )
        for booking in bookings
    ]

    assert 200 == response.status_code
    assert expected_response_data == response.data
