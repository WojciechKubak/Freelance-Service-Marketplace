from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class HealthCheckAPI(APIView):

    def get(self, _: Request) -> Response:
        return Response({"message": "Healthy"}, status=status.HTTP_200_OK)
