"""
Custom permissions
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Special permission class for updating User model
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
