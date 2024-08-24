from rest_framework.permissions import BasePermission
from rest_framework.views import View
from rest_framework.request import Request
from django.db.models import Model


class ResourceOwner(BasePermission):

    def has_object_permission(self, request: Request, _: View, obj: Model) -> bool:
        return obj.created_by == request.user
