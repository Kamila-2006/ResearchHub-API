from rest_framework import permissions
from experiments.models import Experiment


class IsFindingPIOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            experiment_id = request.data.get('experiment')
            if not experiment_id:
                return False
            try:
                experiment = Experiment.objects.get(id=experiment_id)
            except Experiment.DoesNotExist:
                return False
            return request.user.is_authenticated and request.user == experiment.project.principal_investigator
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        experiment = obj.experiment
        pi = experiment.project.principal_investigator
        collaborators = experiment.collaborators.all()

        if request.method in permissions.SAFE_METHODS:
            if obj.visibility == 'public':
                return True
            return (
                request.user.is_authenticated
                and (request.user == pi or request.user in collaborators)
            )

        return request.user.is_authenticated and request.user == pi