from apps.consultations.models import Consultation, Slot, Booking
from apps.consultations.services import SlotService
from apps.users.tests.factories import UserFactory
from apps.categorization.tests.factories import TagFactory, Tag
from factory.django import DjangoModelFactory
from django.utils import timezone
from datetime import timedelta
from typing import Any
import factory


class ConsultationFactory(DjangoModelFactory):
    class Meta:
        model = Consultation
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
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
        lambda: timezone.now() + SlotService.MINIMUM_SLOT_DURATION
    )

    is_cancelled = False

    @factory.post_generation
    def bookings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for booking in extracted:
                self.bookings.add(booking)
        elif extracted is None:
            for _ in range(3):
                BookingFactory(slot=self)

        self.save()


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    start_time = factory.LazyFunction(lambda: timezone.now())
    end_time = factory.LazyFunction(lambda: timezone.now() + timedelta(minutes=30))

    slot = factory.SubFactory(SlotFactory)

    status = Booking.Status.PENDING

    booked_by = factory.SubFactory(UserFactory)
