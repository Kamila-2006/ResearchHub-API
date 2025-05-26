from rest_framework import permissions
from apps.projects.models import Project

class IsExperimentCreatorOrCollaborator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            project_id = request.data.get('project')
            if not project_id:
                return False
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return False
            return request.user == project.principal_investigator
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user == obj.project.principal_investigator
                or request.user in obj.collaborators.all()
            )
        return request.user == obj.project.principal_investigator
