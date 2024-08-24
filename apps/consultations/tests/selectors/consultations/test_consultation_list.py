from apps.consultations.tests.factories import ConsultationFactory
from apps.categorization.tests.factories import CategoryFactory, TagFactory
from apps.consultations.selectors.consultations import consultation_list
import pytest


class TestConsultationList:

    def test_consultation_list_returns_only_visible_data(self) -> None:
        category1 = ConsultationFactory(is_visible=True)
        _ = ConsultationFactory(is_visible=False)

        result = consultation_list()

        assert [category1] == list(result)

    def test_consultation_list_filters_by_related_category_id(self) -> None:
        category1 = CategoryFactory()
        consultation1 = ConsultationFactory(tags=[TagFactory(category=category1)])
        category2 = CategoryFactory()
        _ = ConsultationFactory(tags=[TagFactory(category=category2)])

        result = consultation_list(filters={"category_id": category1.id})

        assert [consultation1] == list(result)

    def test_consultation_list_filters_by_related_tag_id(self) -> None:
        tag1 = TagFactory()
        consultation1 = ConsultationFactory(tags=[tag1])
        tag2 = TagFactory()
        _ = ConsultationFactory(tags=[tag2])

        result = consultation_list(filters={"tag_id": tag1.id})

        assert [consultation1] == list(result)

    def test_consultation_list_filters_one_side_of_price_range(self) -> None:
        consultation1 = ConsultationFactory(price=350)
        consultation2 = ConsultationFactory(price=150)

        result_price_min = consultation_list(filters={"price_min": 330})
        result_price_max = consultation_list(filters={"price_max": 200})

        assert [consultation1] == list(result_price_min)
        assert [consultation2] == list(result_price_max)

    @pytest.mark.parametrize(
        "price_min, price_max, expected_count",
        [
            (100, 200, 1),
            (200, 300, 0),
            (100, 400, 2),
        ],
    )
    def test_consultation_list_filters_by_chained_price_min_and_price_max(
        self, price_min: float, price_max: float, expected_count: int
    ) -> None:
        ConsultationFactory(price=150)
        ConsultationFactory(price=350)

        result = consultation_list(
            filters={"price_min": price_min, "price_max": price_max}
        )

        assert expected_count == result.count()
