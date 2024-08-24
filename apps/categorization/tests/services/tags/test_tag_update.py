from apps.categorization.tests.factories import TagFactory, CategoryFactory
from apps.categorization.services.tags import TAG_MISSING_CATEGORY, tag_update
from apps.categorization.models import Tag
from django.core.exceptions import ValidationError
import pytest


class TestTagUpdate:

    @pytest.mark.django_db
    def test_method_fails_due_to_non_existing_category_id_and_raises_validation_error(
        self,
    ) -> None:
        tag = TagFactory()
        with pytest.raises(ValidationError, match=TAG_MISSING_CATEGORY):
            tag_update(tag=tag, name=f"new_{tag.name}", category_id=999)

    @pytest.mark.django_db
    def test_method_updates_instance_simple_field_and_returns_it(self) -> None:
        tag = TagFactory()
        category = CategoryFactory()
        updated_name = f"new_{tag.name}"

        result = tag_update(
            tag=tag,
            name=updated_name,
            category_id=category.id,
        )

        assert Tag.objects.get(id=result.id) == result
        assert updated_name == result.name

    @pytest.mark.django_db
    def test_method_updates_foreign_key_field_and_returns_it(self) -> None:
        tag = TagFactory()
        category = CategoryFactory()

        result = tag_update(
            tag=tag,
            category_id=category.id,
        )

        assert Tag.objects.get(id=result.id) == result
        assert category.id == result.category.id
