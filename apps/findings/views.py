from rest_framework import viewsets
from django.db import models
from .models import Finding
from .serializers import FindingSerializer
from .pagination import StandardResultsSetPagination
from .permissions import IsFindingPIOrReadOnly


class FindingViewSet(viewsets.ModelViewSet):
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
    permission_classes = [IsFindingPIOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        base_qs = Finding.objects.all()
        if not user.is_authenticated:
            return base_qs.filter(visibility='public')
        from apps.experiments.models import Experiment
        exp_ids = Experiment.objects.filter(
            models.Q(project__principal_investigator=user) | models.Q(collaborators=user)
        ).values_list('id', flat=True)
        return base_qs.filter(
            models.Q(visibility='public') | models.Q(experiment_id__in=exp_ids)
        ).distinct()
