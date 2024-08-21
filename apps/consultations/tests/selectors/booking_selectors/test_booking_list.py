from apps.consultations.tests.factories import BookingFactory
from apps.consultations.selectors import BookingSelectors
from apps.users.tests.factories import UserFactory
import pytest


@pytest.mark.django_db
def test_booking_list_filters_only_user_bookings() -> None:
    user = UserFactory()

    bookings = BookingFactory.create_batch(2, booked_by=user)
    BookingFactory.create_batch(2)

    result = BookingSelectors.booking_list(user=user)

    assert bookings == list(result)
