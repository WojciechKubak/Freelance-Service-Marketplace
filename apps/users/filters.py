from apps.users.models import User
from django_filters import FilterSet


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ["id", "email", "is_admin", "is_active"]
