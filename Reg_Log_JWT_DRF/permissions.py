from rest_framework.permissions import BasePermission


class IsAuthenticatedAdminUser(BasePermission):
    def has_permission(self, request, view):
        """ Allows access only to admin authenticated users. """
        if request.user and request.user.is_authenticated and request.user.role == 'admin':
            return True


class UpdateOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        """ User only Updates Permission """
        if request.method in ['PATCH', 'PUT']:
            return True

    def has_object_permission(self, request, view, obj):
        """ Allow access to the object only for the 'update' method """
        if request.method in ['PATCH', 'PUT']:
            return True
