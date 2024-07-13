from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import Response, exception_handler
from typing import Any


# https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/api/exception_handlers.py
def custom_exception_handler(exc: Exception, ctx: dict[str, Any]) -> Response:
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    return response
