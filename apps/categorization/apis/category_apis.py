from apps.api.utils import inline_serializer
from apps.api.permissions import IsOwner
from apps.categorization.services.category_service import CategoryService
from apps.categorization.models import Category
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status


class CategoryListApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ["id", "name"]

    def get(self, _: Request) -> Response:
        categories = Category.objects.all().order_by("id")
        output_serializer = self.OutputSerializer(categories, many=True)
        return Response(output_serializer.data)


class CategoryCreateApi(APIView):
    permission_classes = (IsAdminUser,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        category = CategoryService.category_create(
            user=request.user, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(category)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def get(self, _: Request, category_id: int) -> Response:
        category = get_object_or_404(Category, id=category_id)
        output_serializer = self.OutputSerializer(category)
        return Response(output_serializer.data)


class CategoryUpdateApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        description = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def put(self, request: Request, category_id: int) -> Response:
        category = get_object_or_404(Category, id=category_id)

        self.check_object_permissions(request, category)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        category = CategoryService.category_update(
            category=category, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(category)
        return Response(output_serializer.data)
