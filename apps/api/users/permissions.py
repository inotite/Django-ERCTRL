from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.profile.is_administrator()
