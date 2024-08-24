from apps.consultations.tests.factories import SlotFactory
from apps.consultations.selectors.slots import slot_detail
from django.http import Http404
import pytest


class TestSlotDetail:

    def test_slot_detail_raises_404_on_non_existing_slot(self) -> None:
        slot = SlotFactory(is_cancelled=True)
        with pytest.raises(Http404):
            slot_detail(slot_id=slot.id)

    def test_slot_detail_returns_obj_on_success(self) -> None:
        slot = SlotFactory()
        result = slot_detail(slot_id=slot.id)
        assert slot == result
