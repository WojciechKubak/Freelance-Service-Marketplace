from apps.api.utils import inline_serializer
from apps.api.permissions import ResourceOwner
from apps.categorization.services.tags import tag_create, tag_update
from apps.categorization.models import Tag
from apps.categorization.selectors import tag_list
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status


class TagListApi(APIView):
    permission_classes = (AllowAny,)

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = ["id", "name"]

    def get(self, request: Request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        tags = tag_list(filters=filter_serializer.validated_data)

        output_serializer = self.OutputSerializer(tags, many=True)
        return Response(output_serializer.data)


class TagCreateApi(APIView):
    permission_classes = (IsAdminUser,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        category_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        category = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            }
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        tag = tag_create(user=request.user, **input_serializer.validated_data)

        output_serializer = self.OutputSerializer(tag)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class TagUpdateApi(APIView):
    permission_classes = (ResourceOwner,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        category_id = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        category = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            }
        )

    def put(self, request: Request, tag_id: int) -> Response:
        tag = get_object_or_404(Tag, id=tag_id)

        self.check_object_permissions(request, tag)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        tag = tag_update(tag=tag, **input_serializer.validated_data)

        output_serializer = self.OutputSerializer(tag)
        return Response(output_serializer.data)
