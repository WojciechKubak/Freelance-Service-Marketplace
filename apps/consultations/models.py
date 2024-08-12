from apps.common.models import BaseModel
from apps.categorization.models import Tag
from apps.users.models import User
from django.db import models


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
    consultation = models.ForeignKey(
        Consultation, related_name="slots", on_delete=models.CASCADE
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_cancelled = models.BooleanField(default=False)

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
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="There might be many bookings for single slot",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )

    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Booking {self.id}"
