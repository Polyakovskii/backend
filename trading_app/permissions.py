"""
Custom permissions
"""
from rest_framework import permissions


class IsOwnerOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Special permission class for updating User model
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return obj == request.user
