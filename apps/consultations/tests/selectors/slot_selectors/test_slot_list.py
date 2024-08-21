from apps.consultations.tests.factories import SlotFactory, ConsultationFactory
from apps.consultations.selectors import SlotSelectors
import pytest


class TestSlotList:

    @pytest.mark.django_db
    def test_slot_list_outfilters_cancelled_slots(self) -> None:
        SlotFactory.create_batch(2, is_cancelled=True)
        visible_slots = SlotFactory.create_batch(2, is_cancelled=False)

        result = SlotSelectors.slot_list()

        assert visible_slots == list(result)

    @pytest.mark.django_db
    def test_slot_list_outfilters_invisible_consultations(self) -> None:
        SlotFactory(consultation__is_visible=False)
        visible_slots = SlotFactory.create_batch(2, consultation__is_visible=True)

        result = SlotSelectors.slot_list()

        assert visible_slots == list(result)

    @pytest.mark.django_db
    def test_slot_returns_all_data_with_no_filters(self) -> None:
        slots = SlotFactory.create_batch(2)
        result = SlotSelectors.slot_list()
        assert slots == list(result)

    @pytest.mark.django_db
    def test_slot_filters_by_related_consultation_id(self) -> None:
        consultation1, consultation2 = ConsultationFactory.create_batch(2)
        slots1 = SlotFactory.create_batch(2, consultation=consultation1)
        SlotFactory.create_batch(2, consultation=consultation2)

        result = SlotSelectors.slot_list(filters={"consultation_id": consultation1.id})

        assert slots1 == list(result)
