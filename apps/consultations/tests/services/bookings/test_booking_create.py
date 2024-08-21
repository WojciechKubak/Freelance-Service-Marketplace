from apps.consultations.tests.factories import SlotFactory, BookingFactory, UserFactory
from apps.consultations.services.bookings import BookingService, SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


class TestBookingCreate:

    @pytest.mark.django_db
    def test_booking_create_raises_meeting_duration_validation_error(
        self,
    ) -> None:
        user = UserFactory()
        # todo: bookings are controlled via generate_bookings flag
        slot = SlotFactory(bookings=[])

        start_time = slot.start_time
        end_time = slot.start_time + timezone.timedelta(minutes=15)

        booking_service = BookingService(slot=slot)

        with pytest.raises(ValidationError) as e:
            booking_service.booking_create(
                user=user, start_time=start_time, end_time=end_time
            )

        assert "Meeting duration must be at least 1 hour." in str(e.value)

    @pytest.mark.django_db
    def test_booking_create_raises_out_of_slot_time_range_validation_error(
        self,
    ) -> None:
        user = UserFactory()
        slot = SlotFactory(bookings=[])

        booking_service = BookingService(slot=slot)

        with pytest.raises(ValidationError) as e:
            booking_service.booking_create(
                user=user,
                start_time=slot.start_time - timezone.timedelta(minutes=30),
                end_time=slot.end_time,
            )

        assert "Booking time must be within the slot time range." in str(e.value)

    @pytest.mark.django_db
    def test_booking_create_raises_booking_overlap_validation_error(
        self,
    ) -> None:
        user = UserFactory()
        booking = BookingFactory()
        slot = SlotFactory(bookings=[booking])

        booking_service = BookingService(slot=slot)

        with pytest.raises(ValidationError) as e:
            booking_service.booking_create(
                user=user, start_time=slot.start_time, end_time=slot.end_time
            )

        assert "Booking overlaps with existing bookings." in str(e.value)

    @pytest.mark.django_db
    def test_booking_create_raises_same_user_booking_model_validation_error(
        self,
    ) -> None:
        slot = SlotFactory(
            bookings=[],
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=3),
        )

        booking_service = BookingService(slot=slot)

        with pytest.raises(ValidationError) as e:
            booking_service.booking_create(
                user=slot.consultation.created_by,
                start_time=slot.start_time,
                end_time=slot.start_time + SlotService.MINIMUM_MEETING_DURATION,
            )

        assert "Cannot book own slot." in str(e.value)

    @pytest.mark.django_db
    def test_booking_create_creates_db_instance_and_returns_it(self) -> None:
        # todo: this slot logic was also implemented in factory
        slot = SlotFactory(
            bookings=[],
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=3),
        )
        user = UserFactory()
        booking_service = BookingService(slot=slot)

        result = booking_service.booking_create(
            user=user,
            start_time=slot.start_time,
            end_time=slot.start_time + SlotService.MINIMUM_MEETING_DURATION,
        )

        assert slot.bookings.first() == result

    @pytest.mark.django_db
    def test_booking_create_calls_create_meeting_function_with_expected_arguments(
        self, mock_create_meeting
    ) -> None:
        slot = SlotFactory(
            bookings=[],
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=3),
        )
        user = UserFactory()
        booking_service = BookingService(slot=slot)

        booking_service.booking_create(
            user=user,
            start_time=slot.start_time,
            end_time=slot.start_time + SlotService.MINIMUM_MEETING_DURATION,
        )

        mock_create_meeting.assert_called_once_with(
            topic=slot.consultation.title,
            start_time=slot.start_time,
            duration=(
                slot.start_time + SlotService.MINIMUM_MEETING_DURATION - slot.start_time
            ).seconds
            // 60,
        )
