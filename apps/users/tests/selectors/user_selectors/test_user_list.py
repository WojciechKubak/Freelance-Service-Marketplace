from apps.users.selectors import UserSelectors
from apps.users.models import User
import pytest


class TestUserList:

    @pytest.mark.django_db
    def test_user_list_returns_no_results_with_filter_provided(self) -> None:
        email = "email@example.com"
        User.objects.create_user(email=email)

        filters = {"email": f"other_{email}"}

        assert not UserSelectors.user_list(filters=filters)

    @pytest.mark.django_db
    def test_user_list_returns_single_result_with_filter_provided(self) -> None:
        email = "email@example.com"
        User.objects.create_user(email=email)

        filters = {"email": email}

        result = UserSelectors.user_list(filters=filters)

        assert 1 == result.count()

    @pytest.mark.django_db
    def test_user_list_returns_multiple_results_with_filter_provided(self) -> None:
        User.objects.create_user(email="first@example.com", is_admin=True)
        User.objects.create_user(email="second@example.com", is_admin=True)

        filters = {"is_admin": True}

        result = UserSelectors.user_list(filters=filters)

        assert 2 == result.count()

    @pytest.mark.django_db
    def test_user_list_returns_all_users_without_filters_provided(self) -> None:
        User.objects.create_user(email="first@example.com")
        User.objects.create_user(email="second@example.com")

        result = UserSelectors.user_list(filters={})

        assert 2 == result.count()
