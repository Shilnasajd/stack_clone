# from rest_framework.permissions import BasePermission
from rest_framework import permissions
class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user==obj.user

# safe_method   GET,HEAD,OPTIONS,LIST,DETAIL
# unsafe_method PUT PATCH ,DELETE