from rest_framework import permissions

class IsGroupLeaderOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'members'):
            return obj.members.filter(user=user, role='leader', is_active=True).exists()

        if hasattr(obj, 'group'):
            return obj.group.members.filter(user=user, role='leader', is_active=True).exists()

        return False
