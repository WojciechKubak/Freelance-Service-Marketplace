from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class HealthCheckAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, _: Request) -> Response:
        return Response({"status": "Healthy"}, status=status.HTTP_200_OK)
