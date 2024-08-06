from apps.consultations.services import ConsultationService
from apps.consultations.models import Consultation
from apps.api.permissions import IsOwner
from apps.api.utils import inline_serializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404


class ConsultationCreateApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = serializers.ListField(
            child=serializers.IntegerField(), min_length=1, max_length=5
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
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
        description = serializers.CharField(required=False)
        price = serializers.FloatField(required=False)
        tags = serializers.ListField(child=serializers.IntegerField(), required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
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
