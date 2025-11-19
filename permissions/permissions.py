from rest_framework import permissions

class HasResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True

        resource_name = getattr(view, 'resource_name', None)
        if not resource_name:
            # If the view doesn't define a resource, we assume it's not protected by this specific permission class
            return True
        
        method_action_map = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        
        action_name = method_action_map.get(request.method)
        if not action_name:
            return False
        
        # Check if user has this permission via roles
        return request.user.roles.filter(
            permissions__resource__code=resource_name,
            permissions__action__code=action_name
        ).exists()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
