from apps.api.pagination import get_paginated_response
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

        response = get_paginated_response(
            queryset=users,
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            request=request,
        )

        return response


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


class UserActivateApi(APIView):
    permission_classes = (AllowAny,)

    def get(self, _: Request, user_id: str) -> Response:
        UserService.user_activate(signed_value=user_id)
        return Response(status=status.HTTP_200_OK)


class UserActivationEmailResendApi(APIView):
    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService.user_activation_email_resend(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
