from apps.categorization.tests.factories import TagFactory, CategoryFactory
from apps.categorization.selectors import TagSelectors
import pytest


class TestTagList:

    @pytest.mark.django_db
    def test_selector_on_empty_filters_return_all_data(self) -> None:
        tags = TagFactory.create_batch(3)
        result = TagSelectors.tag_list(filters={})
        assert tags == list(result)

    @pytest.mark.django_db
    def test_selector_on_single_simple_field_filter(self) -> None:
        tags = TagFactory.create_batch(3)

        filter_found = {"name": tags[0].name}
        filter_not_found = {"name": f"other_{tags[0].name}"}

        result_found = TagSelectors.tag_list(filters=filter_found)
        result_not_found = TagSelectors.tag_list(filters=filter_not_found)

        assert [tags[0]] == list(result_found)
        assert [] == list(result_not_found)

    @pytest.mark.django_db
    def test_selector_on_chained_simple_fields_filter(self) -> None:
        category = CategoryFactory()
        tags = TagFactory.create_batch(3, category=category)

        filter_found = {"name": tags[0].name, "category": category.name}
        filter_not_found = {
            "name": f"other_{tags[0].name}",
            "category": f"other_{category.name}",
        }

        result_found = TagSelectors.tag_list(filters=filter_found)
        result_not_found = TagSelectors.tag_list(filters=filter_not_found)

        assert [tags[0]] == list(result_found)
        assert [] == list(result_not_found)