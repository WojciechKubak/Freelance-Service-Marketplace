from apps.users.models import User
from apps.users.selectors import UserSelectors
from apps.users.services import UserService
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework import serializers


class UserListApi(APIView):
    permission_classes = (IsAdminUser,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100
        page_size_query_param = "count"

    class FilterSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=False)
        email = serializers.EmailField(required=False)
        is_admin = serializers.BooleanField(
            required=False, allow_null=True, default=None
        )
        is_active = serializers.BooleanField(
            required=False, allow_null=True, default=None
        )

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email", "is_admin", "is_active"]

    def get(self, request: Request) -> Response:
        filters = self.FilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)

        users = UserSelectors.user_list(filters=filters.validated_data)

        paginator = self.Pagination()
        paginated_users = paginator.paginate_queryset(users, request)

        if paginated_users is not None:
            serializer = self.OutputSerializer(paginated_users, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterApi(APIView):
    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["email", "is_admin", "is_active"]

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.user_create(**serializer.validated_data)

        output_serializer = self.OutputSerializer(user)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
