from apps.users.models import User
from apps.users.filters import UserFilter
from django.db.models import QuerySet


def user_list(*, filters: dict[str, str | bool] = None) -> QuerySet:
    filters = filters or {}
    queryset = User.objects.all()

    return UserFilter(filters, queryset).qs
