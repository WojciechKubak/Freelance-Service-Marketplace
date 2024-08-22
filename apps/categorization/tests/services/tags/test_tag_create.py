from apps.categorization.tests.factories import UserFactory, CategoryFactory
from apps.categorization.models import Tag
from apps.categorization.services.tags import tag_create
from django.core.exceptions import ValidationError
import pytest


class TestTagCreate:
    simple_field_data: dict[str, str] = {"name": "Tag 1"}

    @pytest.mark.django_db
    def test_method_fails_due_to_not_existing_category_and_raises_object_does_not_exist(
        self,
    ) -> None:
        user = UserFactory()
        data = {
            **self.simple_field_data,
            "category_id": 999,
            "user": user,
        }

        with pytest.raises(ValidationError):
            tag_create(**data)

    @pytest.mark.django_db
    def test_method_creates_instance_with_expected_data_and_returns_it(
        self,
    ) -> None:
        category = CategoryFactory()
        user = UserFactory()
        data = {
            **self.simple_field_data,
            "category_id": category.id,
            "user": user,
        }

        result = tag_create(**data)

        assert Tag.objects.get(id=result.id) == result

        assert data["name"] == result.name
        assert data["category_id"] == result.category.id
        assert data["user"].id == str(result.created_by.id)
