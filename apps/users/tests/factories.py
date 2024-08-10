from factory.django import DjangoModelFactory
from apps.users.models import User
import factory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")

    email = factory.Faker("email")
    password = factory.django.Password("password")

    is_active = True
    is_admin = False
