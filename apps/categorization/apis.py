from apps.categorization.models import Category
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers


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
