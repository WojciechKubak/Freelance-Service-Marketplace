from apps.consultations.models import Consultation
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
