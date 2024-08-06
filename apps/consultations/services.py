from apps.consultations.models import Consultation
from apps.categorization.models import Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
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
