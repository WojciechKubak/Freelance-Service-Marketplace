from apps.consultations.services import ConsultationService
from apps.api.utils import inline_serializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status


class ConsultationCreateApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = serializers.ListField(child=serializers.IntegerField())

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
