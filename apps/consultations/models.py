from apps.common.models import BaseModel
from apps.categorization.models import Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class Consultation(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    tags = models.ManyToManyField(Tag)

    is_visible = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("created_by",)

    def __str__(self) -> str:
        return f"Consultation {self.title}"


class Slot(BaseModel):

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"
        BLOCKED = "blocked", "Blocked"

    consultation = models.ForeignKey(
        Consultation, related_name="slots", on_delete=models.CASCADE
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    class Meta:
        ordering = ("start_time",)
        constraints = (
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="slot_start_time_lt_end_time",
            ),
        )

    def __str__(self) -> str:
        return f"Slot at {self.start_time}"


class Booking(BaseModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="OTM relationship - slot is available after cancellation",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("slot", "booked_by")

    def __str__(self) -> str:
        return f"Booking {self.id}"

    def clean(self) -> None:
        super().clean()
        if not (self.slot.start_time <= self.start_time < self.slot.end_time):
            raise ValidationError(
                "Booking start time must be within the slot time range."
            )
        if not (self.slot.start_time < self.end_time <= self.slot.end_time):
            raise ValidationError(
                "Booking end time must be within the slot time range."
            )
