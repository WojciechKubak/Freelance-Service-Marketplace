from apps.consultations.services import ConsultationService
from apps.consultations.selectors import ConsultationSelectors
from apps.consultations.models import Consultation
from apps.api.permissions import IsOwner
from apps.api.utils import inline_serializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404


class ConsultationCreateApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        content = serializers.CharField()
        price = serializers.FloatField()
        tags = serializers.ListField(
            child=serializers.IntegerField(), min_length=1, max_length=5
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.consultation_create(
            user=request.user, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ConsultationUpdateApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        content = serializers.CharField(required=False)
        price = serializers.FloatField(required=False)
        tags = serializers.ListField(child=serializers.IntegerField(), required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def post(self, request: Request, consultation_id: int) -> Response:
        consultation = get_object_or_404(Consultation, id=consultation_id)

        self.check_object_permissions(request, consultation)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.consultation_update(
            consultation, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data)


class ConsultationChangeVisibilityApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        is_visible = serializers.BooleanField(required=True)

    def patch(self, request: Request, consultation_id: int) -> Response:
        consultation = get_object_or_404(Consultation, id=consultation_id)
        self.check_object_permissions(request, consultation)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        ConsultationService.consultation_change_visibility(
            consultation, is_visible=input_serializer.validated_data["is_visible"]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsultationListApi(APIView):
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100
        page_size_query_param = "count"

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        category_id = serializers.IntegerField(required=False)
        tag_id = serializers.IntegerField(required=False)
        price_min = serializers.FloatField(required=False)
        price_max = serializers.FloatField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def get(self, request: Request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        consultations = ConsultationSelectors.consultation_list(
            filters=filter_serializer.validated_data
        )

        # todo: missing pagination call here
        output_serializer = self.OutputSerializer(consultations, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ConsultationDetailApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        content = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def get(self, _: Request, consultation_id: int) -> Response:
        consultation = ConsultationSelectors.consultation_detail(
            consultation_id=consultation_id
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
