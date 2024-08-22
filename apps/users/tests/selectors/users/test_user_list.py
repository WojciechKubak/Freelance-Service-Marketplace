from apps.users.tests.factories import UserFactory
from apps.users.selectors import user_list
import pytest


class TestUserList:

    @pytest.mark.django_db
    def test_user_list_returns_no_results_with_filter_provided(self) -> None:
        email = "email@example.com"
        UserFactory(email=email)

        filters = {"email": f"other_{email}"}

        assert not user_list(filters=filters)

    @pytest.mark.django_db
    def test_user_list_returns_single_result_with_filter_provided(self) -> None:
        email = "email@example.com"
        UserFactory(email=email)

        filters = {"email": email}

        result = user_list(filters=filters)

        assert 1 == result.count()

    @pytest.mark.django_db
    def test_user_list_returns_multiple_results_with_filter_provided(self) -> None:
        UserFactory.create_batch(2, is_admin=True)

        filters = {"is_admin": True}

        result = user_list(filters=filters)

        assert 2 == result.count()

    @pytest.mark.django_db
    def test_user_list_returns_all_users_without_filters_provided(self) -> None:
        UserFactory.create_batch(2)

        result = user_list(filters={})

        assert 2 == result.count()
