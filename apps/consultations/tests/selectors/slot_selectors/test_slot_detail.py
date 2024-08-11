from apps.consultations.tests.factories import SlotFactory
from apps.consultations.selectors import SlotSelectors
from django.http import Http404
import pytest


class TestSlotDetail:

    @pytest.mark.django_db
    def test_slot_detail_raises_404_on_non_existing_slot(self) -> None:
        slot = SlotFactory(is_cancelled=True)
        with pytest.raises(Http404):
            SlotSelectors.slot_detail(slot_id=slot.id)

    @pytest.mark.django_db
    def test_slot_detail_returns_obj_on_success(self) -> None:
        slot = SlotFactory()
        result = SlotSelectors.slot_detail(slot_id=slot.id)
        assert slot == result
