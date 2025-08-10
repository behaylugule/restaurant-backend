from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):

     
    def has_permission(self, request, view):
        # Deny access if not authenticated
        if not request.user.is_authenticated:
            return False

        # Allow access if the user is either a superuser or a staff member
        return request.user.role == 'admin'
