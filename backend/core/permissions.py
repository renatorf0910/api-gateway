from rest_framework.permissions import BasePermission

class HasKeycloakRole(BasePermission):
    required_role = "admin"

    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        roles = token.get("realm_access", {}).get("roles", [])
        return self.required_role in roles
