from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET']


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in SAFE_METHODS
