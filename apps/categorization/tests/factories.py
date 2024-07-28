from apps.users.tests.factories import UserFactory
from apps.categorization.models import Category, Tag
from factory.django import DjangoModelFactory
from typing import Any
import factory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        skip_postgeneration_save = True

    name = factory.Faker("word")
    description = factory.Faker("sentence")
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

        tag.save()


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)
