from rest_framework.permissions import BasePermission
from .methods import ActionNotAllowed


class CanCreateArticlePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name__in=['Admin', 'Writer']).exists():
            return True
        else:
            raise ActionNotAllowed(
                "You do not have permission to register a school.")


class IsOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name__in=['Admin', 'Mod']).exists():
            return True
        else:
            raise ActionNotAllowed(
                "You do not have permission to register a school.")
