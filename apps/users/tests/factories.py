from factory.django import DjangoModelFactory
from apps.users.models import User
import factory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    email = factory.Faker("email")
    password = factory.django.Password("password")
    # todo: we might want to set this to True by default
    is_active = factory.Faker("boolean")
    is_admin = factory.Faker("boolean")
