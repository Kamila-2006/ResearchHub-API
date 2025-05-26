from rest_framework import permissions
from apps.projects.models import Project

class IsProjectPrincipalInvestigatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.principal_investigator == request.user


class IsProjectMemberPrincipalInvestigatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            project_id = request.data.get('project')
            if not project_id:
                return False
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return False
            return project.principal_investigator == request.user
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.principal_investigator == request.user
