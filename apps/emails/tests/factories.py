from apps.emails.models import Email, Status
from django.utils import timezone
import factory


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    status = Status.READY
    to = factory.Faker("email")
    subject = factory.Faker("sentence", nb_words=6)
    html = factory.Faker("paragraph", nb_sentences=3)
    plain_text = factory.Faker("paragraph", nb_sentences=3)
    sent_at = factory.LazyAttribute(
        lambda o: timezone.now() if o.status == Status.SENT else None
    )
