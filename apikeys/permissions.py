from rest_framework import permissions
from .models import UserApiKey

class HasUserAPIKey(permissions.BasePermission):
    def has_permission(self, request, view):
        # Explicitly fetch the header from META
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Verify format: "Api-Key <key>"
        if not auth.startswith('Api-Key '):
            return False
            
        key = auth.split(' ')[1]
        
        # Manually verify against your UserApiKey model
        return UserApiKey.objects.is_valid(key)