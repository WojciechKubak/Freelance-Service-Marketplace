from apps.consultations.models import Consultation, Slot
from apps.categorization.models import Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
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
        description: str,
        price: float,
        tags: list[int],
    ) -> Consultation:

        existing_tags = Tag.objects.filter(id__in=tags)
        if existing_tags.count() != len(tags):
            raise ValidationError("One or more tags do not exist.")

        consultation = Consultation(
            title=title, description=description, price=price, created_by=user
        )

        consultation.full_clean()
        consultation.save()

        consultation.tags.add(*existing_tags)

        return consultation

    @staticmethod
    def consultation_update(
        consultation: Consultation,
        title: str | None = None,
        description: str | None = None,
        price: float | None = None,
        tags: list[int] | None = None,
    ) -> Consultation:

        if tags:
            existing_tags = Tag.objects.filter(id__in=tags)
            if existing_tags.count() != len(tags):
                raise ValidationError("One or more tags do not exist.")

            consultation.tags.clear()
            consultation.tags.add(*existing_tags)

        consultation.title = title if title else consultation.title
        consultation.description = (
            description if description else consultation.description
        )
        consultation.price = price if price else consultation.price

        consultation.full_clean()
        consultation.save()

        return consultation

    @staticmethod
    def consultation_change_visibility(
        consultation: Consultation, is_visible: bool = False
    ) -> Consultation:
        consultation.is_visible = is_visible
        consultation.save()

        return consultation


@dataclass
class SlotService:
    MINIMUM_SLOT_DURATION: ClassVar[timedelta] = timedelta(hours=1)
    consultation: Consultation

    def slot_create(self, *, start_time: datetime, end_time: datetime) -> Slot:
        self._slot_validate_visibility()
        self._slot_validate_duration(start_time=start_time, end_time=end_time)
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

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)

        slot.start_time = start_time if start_time else slot.start_time
        slot.end_time = end_time if end_time else slot.end_time

        self._slot_validate_duration(start_time=slot.start_time, end_time=slot.end_time)
        self._slot_validate_overlap(
            start_time=slot.start_time, end_time=slot.end_time, slot_id=slot.id
        )

        slot.full_clean()
        slot.save()

        return slot

    # todo: move error messages to constants
    def _slot_validate_visibility(self) -> None:
        if not self.consultation.is_visible:
            raise ValidationError("Consultation is not visible.")

    def _slot_validate_duration(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        if end_time - start_time < SlotService.MINIMUM_SLOT_DURATION:
            raise ValidationError("Slot duration must be at least 1 hour.")

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
