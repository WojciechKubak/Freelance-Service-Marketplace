from apps.users.tests.factories import UserFactory
from apps.categorization.models import Category, Tag
from factory.django import DjangoModelFactory
import factory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    created_by = factory.SubFactory(UserFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(UserFactory)
