from apps.users.tests.factories import UserFactory
from apps.users.models import User
from apps.api.pagination import get_paginated_response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from collections import OrderedDict
import pytest


class ExampleListView(APIView):
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email"]

    def get(self, request: Request) -> Response:
        queryset = User.objects.all().order_by("email")

        response = get_paginated_response(
            queryset=queryset,
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            request=request,
        )

        return response


class TestGetPaginatedResponse:

    @pytest.mark.django_db
    def test_response_is_paginated_correctly(self) -> None:
        users = UserFactory.create_batch(2)
        first, second = sorted(users, key=lambda user: user.email)

        factory = APIRequestFactory()

        request = factory.get("/api/users/")
        response = ExampleListView.as_view()(request)

        expected_response_first_page = OrderedDict(
            {
                "count": 2,
                "next": "http://testserver/api/users/?limit=1&offset=1",
                "previous": None,
                "results": [{"id": str(first.id), "email": first.email}],
            }
        )

        assert expected_response_first_page == response.data

        request = factory.get("/api/users/?limit=1&offset=1")
        response = ExampleListView.as_view()(request)

        expected_response_second_page = OrderedDict(
            {
                "count": 2,
                "next": None,
                "previous": "http://testserver/api/users/?limit=1",
                "results": [{"id": str(second.id), "email": second.email}],
            }
        )

        assert expected_response_second_page == response.data
