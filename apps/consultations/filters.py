from apps.consultations.models import Consultation, Slot
from django_filters import FilterSet
import django_filters


class ConsultationFilter(FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    category_id = django_filters.NumberFilter(
        field_name="tags__category__id", lookup_expr="exact"
    )
    tag_id = django_filters.NumberFilter(field_name="tags__id", lookup_expr="exact")

    class Meta:
        model = Consultation
        fields = [
            "title",
            "price_min",
            "price_max",
            "category_id",
            "tag_id",
        ]


class SlotFilter(FilterSet):
    consultation_id = django_filters.NumberFilter(
        field_name="consultation__id", lookup_expr="exact"
    )
    start_time = django_filters.DateTimeFilter(
        field_name="start_time", lookup_expr="gte"
    )
    end_time = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")

    class Meta:
        model = Slot
        fields = [
            "consultation_id",
            "start_time",
            "end_time",
        ]
