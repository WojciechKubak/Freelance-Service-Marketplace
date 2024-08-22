from apps.consultations.tests.factories import SlotFactory, UserFactory
from apps.consultations.services.bookings import (
    BOOKING_CANNOT_BOOK_OWN_SLOT,
    BOOKING_VALIDATE_MINIMAL_DURATION_TIME,
    BOOKING_VALIDATE_OVERLAP,
    BOOKING_VALIDATE_WITHING_SLOT_RANGE,
    BookingService,
)
from apps.users.models import User
from apps.consultations.apis.bookings import BookingCreateApi
from rest_framework.test import APIRequestFactory
from django.utils import timezone
from typing import Callable, Any
from collections import OrderedDict
import pytest


class TestBookingCreateApi:

    @pytest.mark.django_db
    def test_api_response_on_meeting_duration_validation_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(generate_bookings=False)

        request = auth_request(
            user,
            "POST",
            "/api/consultations/bookings/",
            {
                "slot_id": slot.id,
                "start_time": slot.start_time,
                "end_time": slot.start_time
                + timezone.timedelta(
                    minutes=BookingService.BOOKING_MINIMAL_DURATION_TIME_MINUTES - 1
                ),
            },
        )

        response = BookingCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {
                "non_field_errors": [
                    BOOKING_VALIDATE_MINIMAL_DURATION_TIME.format(
                        BookingService.BOOKING_MINIMAL_DURATION_TIME_MINUTES
                    )
                ]
            }
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_out_of_slot_time_range_validation_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(bookings=[])

        request = auth_request(
            user,
            "POST",
            "/api/consultations/bookings/",
            {
                "slot_id": slot.id,
                "start_time": slot.start_time - timezone.timedelta(hours=1),
                "end_time": slot.start_time,
            },
        )

        response = BookingCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": [BOOKING_VALIDATE_WITHING_SLOT_RANGE]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_booking_overlap_validation_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(generate_bookings=True)

        request = auth_request(
            user,
            "POST",
            "/api/consultations/bookings/",
            {
                "slot_id": slot.id,
                "start_time": slot.bookings.first().start_time,
                "end_time": slot.bookings.first().end_time,
            },
        )

        response = BookingCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": [BOOKING_VALIDATE_OVERLAP]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_same_user_booking_model_validation_error(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(consultation__created_by=user)

        request = auth_request(
            user,
            "POST",
            "/api/consultations/bookings/",
            {
                "slot_id": slot.id,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
            },
        )

        response = BookingCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"non_field_errors": [BOOKING_CANNOT_BOOK_OWN_SLOT]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_succesful_booking_create(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
        mock_create_meeting,
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(generate_bookings=False)

        request = auth_request(
            user,
            "POST",
            "/api/consultations/bookings/",
            {
                "slot_id": slot.id,
                "start_time": slot.start_time,
                "end_time": slot.start_time
                + timezone.timedelta(
                    minutes=BookingService.BOOKING_MINIMAL_DURATION_TIME_MINUTES
                ),
            },
        )

        response = BookingCreateApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "id": 1,
                "start_time": slot.start_time.isoformat().replace("+00:00", "Z"),
                "end_time": (
                    slot.start_time
                    + timezone.timedelta(
                        minutes=BookingService.BOOKING_MINIMAL_DURATION_TIME_MINUTES
                    )
                )
                .isoformat()
                .replace("+00:00", "Z"),
                "url": mock_create_meeting.return_value.join_url,
                "slot": OrderedDict(
                    {
                        "id": slot.id,
                        "start_time": slot.start_time.isoformat().replace(
                            "+00:00", "Z"
                        ),
                        "end_time": slot.end_time.isoformat().replace("+00:00", "Z"),
                        "consultation": OrderedDict(
                            {
                                "id": slot.consultation.id,
                                "title": slot.consultation.title,
                                "price": float(slot.consultation.price),
                                "tags": [
                                    OrderedDict(
                                        {
                                            "id": tag.id,
                                            "name": tag.name,
                                        }
                                    )
                                    for tag in slot.consultation.tags.all()
                                ],
                            }
                        ),
                    }
                ),
            }
        )

        assert 201 == response.status_code
        assert expected_response_data == response.data
