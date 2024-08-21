from apps.consultations.models import Consultation, Slot, Booking
from apps.consultations.utils import file_name_generate, text_to_file_local_upload
from apps.integrations.zoom.client import create_meeting
from apps.integrations.aws.client import text_to_file_upload
from apps.storages.enums import StorageType
from apps.categorization.models import Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta
from typing import ClassVar
from dataclasses import dataclass


@dataclass
class ConsultationService:

    @staticmethod
    def consultation_create(
        user: User,
        title: str,
        content: str,
        price: float,
        tags: list[int],
    ) -> Consultation:
        existing_tags = Tag.objects.filter(id__in=tags)
        if existing_tags.count() != len(tags):
            raise ValidationError("One or more tags do not exist.")

        file_name = file_name_generate()

        if settings.STORAGE_TYPE_STRATEGY == StorageType.S3:
            text_to_file_upload(file_name=file_name, content=content)
        else:
            text_to_file_local_upload(file_name=file_name, content=content)

        consultation = Consultation(
            title=title, price=price, created_by=user, content_path=file_name
        )
        consultation.full_clean()
        consultation.save()
        consultation.tags.add(*existing_tags)

        return consultation

    @staticmethod
    def consultation_update(
        consultation: Consultation,
        title: str | None = None,
        content: str | None = None,
        price: float | None = None,
        tags: list[int] | None = None,
    ) -> Consultation:

        if tags:
            existing_tags = Tag.objects.filter(id__in=tags)
            if existing_tags.count() != len(tags):
                raise ValidationError("One or more tags do not exist.")

            consultation.tags.clear()
            consultation.tags.add(*existing_tags)

        if content:
            if settings.STORAGE_TYPE_STRATEGY == StorageType.S3:
                text_to_file_upload(
                    file_name=consultation.content_path, content=content
                )
            else:
                text_to_file_local_upload(
                    file_name=consultation.content_path, content=content
                )

        consultation.title = title if title else consultation.title
        consultation.price = price if price else consultation.price

        consultation.full_clean()
        consultation.save()

        return consultation

    @staticmethod
    def consultation_change_visibility(
        consultation: Consultation, is_visible: bool = False
    ) -> Consultation:
        # todo: this will also affect slots and bookings in some way
        consultation.is_visible = is_visible
        consultation.save()

        return consultation


@dataclass
class SlotService:
    # todo: set this to hour unit also might export?
    MINIMUM_MEETING_DURATION: ClassVar[timedelta] = timedelta(hours=1)
    consultation: Consultation

    @staticmethod
    def meeting_validate_duration(*, start_time: datetime, end_time: datetime) -> None:
        if end_time - start_time < SlotService.MINIMUM_MEETING_DURATION:
            raise ValidationError("Meeting duration must be at least 1 hour.")

    def slot_create(self, *, start_time: datetime, end_time: datetime) -> Slot:
        self._slot_validate_visibility()
        self.meeting_validate_duration(start_time=start_time, end_time=end_time)
        self._slot_validate_overlap(start_time=start_time, end_time=end_time)

        slot = Slot(
            consultation=self.consultation, start_time=start_time, end_time=end_time
        )
        slot.full_clean()
        slot.save()

        return slot

    def slot_update(
        self,
        slot: Slot,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> Slot:
        # todo: we might move this to __post_init__
        self._slot_validate_visibility()

        slot.start_time = start_time if start_time else slot.start_time
        slot.end_time = end_time if end_time else slot.end_time

        self.meeting_validate_duration(
            start_time=slot.start_time, end_time=slot.end_time
        )
        self._slot_validate_overlap(
            start_time=slot.start_time, end_time=slot.end_time, slot_id=slot.id
        )

        slot.full_clean()
        slot.save()

        return slot

    def slot_delete(self, slot: Slot) -> None:
        bookings = slot.bookings.all()
        if bookings.exists():
            bookings.update(status=Booking.Status.CANCELLED)
            slot.is_cancelled = True
            slot.save()
        else:
            slot.delete()

    # todo: move error messages to constants
    def _slot_validate_visibility(self) -> None:
        if not self.consultation.is_visible:
            raise ValidationError("Consultation is not visible.")

    def _slot_validate_overlap(
        self, *, start_time: datetime, end_time: datetime, slot_id: int | None = None
    ) -> None:
        start_time_overlap = Q(start_time__lt=end_time, start_time__gte=start_time)
        end_time_overlap = Q(end_time__gt=start_time, end_time__lte=end_time)
        overlap_query = self.consultation.slots.filter(
            start_time_overlap | end_time_overlap
        )

        if slot_id:
            overlap_query = overlap_query.exclude(id=slot_id)

        if overlap_query.exists():
            raise ValidationError("Slot overlaps with existing slots.")


@dataclass
class BookingService:
    slot: Slot

    def booking_create(
        self, *, user: User, start_time: datetime, end_time: datetime
    ) -> Booking:
        if self.slot.consultation.created_by == user:
            raise ValidationError("Cannot book own slot.")

        SlotService.meeting_validate_duration(start_time=start_time, end_time=end_time)
        self._booking_validate_in_slot_range(start_time=start_time, end_time=end_time)
        self._booking_validate_overlap(start_time=start_time, end_time=end_time)

        meeting_details = create_meeting(
            topic=self.slot.consultation.title,
            start_time=start_time,
            duration=(end_time - start_time).seconds // 60,
        )

        booking = Booking(
            slot=self.slot,
            booked_by=user,
            start_time=start_time,
            end_time=end_time,
            url=meeting_details.join_url,
        )
        booking.full_clean()
        booking.save()

        return booking

    def _booking_validate_in_slot_range(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        if not (self.slot.start_time <= start_time < self.slot.end_time) or not (
            self.slot.start_time < end_time <= self.slot.end_time
        ):
            raise ValidationError("Booking time must be within the slot time range.")

    def _booking_validate_overlap(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        # todo: might merge with _slot_validate_overlap
        start_time_overlap = Q(start_time__lt=end_time, start_time__gte=start_time)
        end_time_overlap = Q(end_time__gt=start_time, end_time__lte=end_time)
        overlap_query = self.slot.bookings.filter(start_time_overlap | end_time_overlap)

        if overlap_query.exists():
            raise ValidationError("Booking overlaps with existing bookings.")