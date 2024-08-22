from apps.core.exceptions import ApplicationError
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.signing import BadSignature, SignatureExpired
from django.http import Http404
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import Response, exception_handler
from typing import Any


def custom_exception_handler(exc: Exception, ctx: dict[str, Any]) -> Response:
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, (BadSignature, SignatureExpired)):
        exc = exceptions.AuthenticationFailed(detail="Invalid or expired signature")

    if isinstance(exc, ApplicationError):
        exc = exceptions.APIException(detail=exc.message)

    response = exception_handler(exc, ctx)

    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    return response
