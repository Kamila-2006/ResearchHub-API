from rest_framework import viewsets, filters
from .models import Experiment
from .serializers import ExperimentSerializer
from .paginations import ExperimentPagination
from .permissions import IsExperimentCreatorOrCollaborator


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [IsExperimentCreatorOrCollaborator]
    pagination_class = ExperimentPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'status']
    ordering_fields = ['start_date', 'end_date', 'title']
