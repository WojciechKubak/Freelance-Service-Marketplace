from apps.common.models import BaseModel
from django.db import models


class Status(models.TextChoices):
    # We move this out of model class to access Status in constraints
    READY = "READY", "Ready"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"


class Email(BaseModel):
    Status = Status

    status = models.CharField(max_length=50, choices=Status, default=Status.READY)

    to = models.EmailField()
    subject = models.CharField(max_length=255)

    html = models.TextField()
    plain_text = models.TextField()

    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(sent_at__isnull=True) | models.Q(status=Status.SENT),
                name="check_email_sent_at_with_status",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.subject} to {self.to}"
