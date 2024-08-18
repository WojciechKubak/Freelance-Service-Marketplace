from apps.consultations.models import Consultation, Slot, Booking
from apps.consultations.services import SlotService
from apps.users.tests.factories import UserFactory
from apps.categorization.tests.factories import TagFactory, Tag
from factory.django import DjangoModelFactory
from django.db.models import Model
from django.utils import timezone
from datetime import datetime, timedelta
from typing import Any
import uuid
import random
import factory


def generate_time_slots(
    start_time: datetime, duration: timedelta, n: int
) -> list[tuple[datetime, datetime]]:
    time_slots = []
    current_start_time = start_time

    for _ in range(n):
        current_end_time = current_start_time + duration
        time_slots.append((current_start_time, current_end_time))
        current_start_time = current_end_time

    return time_slots


class ConsultationFactory(DjangoModelFactory):
    class Meta:
        model = Consultation
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    content_path = uuid.uuid4().hex
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)

    created_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(
        self, create: bool, extracted: list[Tag], **kwargs: dict[str, Any]
    ) -> None:
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            for _ in range(3):
                tag = TagFactory()
                self.tags.add(tag)


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Slot
        skip_postgeneration_save = True

    consultation = factory.SubFactory(ConsultationFactory)

    start_time = factory.LazyFunction(lambda: timezone.now())
    end_time = factory.LazyFunction(
        lambda: timezone.now()
        + SlotService.MINIMUM_MEETING_DURATION * random.randint(4, 8)
    )

    is_cancelled = False

    @classmethod
    def _create(
        cls, model_class: type[Model], *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> Model:
        generate_bookings = kwargs.pop("generate_bookings", False)
        instance = super()._create(model_class, *args, **kwargs)

        if generate_bookings:
            time_slots = generate_time_slots(
                start_time=instance.start_time,
                duration=SlotService.MINIMUM_MEETING_DURATION,
                n=3,
            )
            for start, end in time_slots:
                Booking.objects.create(
                    slot=instance,
                    start_time=start,
                    end_time=end,
                    booked_by=instance.consultation.created_by,
                )

        return instance

    @factory.post_generation
    def bookings(
        self, create: bool, extracted: list[Booking], **kwargs: dict[str, Any]
    ) -> None:
        if not create:
            return

        if extracted == []:
            return

        if extracted:
            for booking in extracted:
                self.bookings.add(booking)


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    slot = factory.SubFactory(SlotFactory)
    status = Booking.Status.CONFIRMED
    url = factory.Faker("url")

    booked_by = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def start_time(self) -> datetime:
        return self.slot.start_time

    @factory.lazy_attribute
    def end_time(self) -> datetime:
        return self.slot.start_time + SlotService.MINIMUM_MEETING_DURATION
