from rest_framework.permissions import BasePermission
from rest_framework.views import View
from rest_framework.request import Request
from django.db.models import Model


class IsOwner(BasePermission):

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        # todo: might prepare dummy view for testing that
        return obj.created_by == request.user
