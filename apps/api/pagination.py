from rest_framework.pagination import BasePagination
from rest_framework.serializers import BaseSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models import QuerySet


def get_paginated_response(
    *,
    queryset: QuerySet,
    pagination_class: type[BasePagination],
    serializer_class: type[BaseSerializer],
    request: Request
) -> Response:
    paginator = pagination_class()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    if paginated_queryset is not None:
        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
