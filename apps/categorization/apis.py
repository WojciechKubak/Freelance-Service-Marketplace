from apps.api.utils import inline_serializer
from apps.categorization.models import Category
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from django.shortcuts import get_object_or_404


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
