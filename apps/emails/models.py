from apps.common.models import BaseModel
from django.db import models


class Email(BaseModel):

    class Type(models.TextChoices):
        ACTIVATE = "ACTIVATE", "activate"
        RESET = "RESET", "reset"
        DELETE = "DELETE", "delete"

    type = models.CharField(max_length=50, choices=Type.choices)

    to = models.EmailField()
    subject = models.CharField(max_length=255)

    sent_at = models.DateTimeField(null=True, blank=True)
