from rest_framework import viewsets, permissions, filters
from .models import Experiment
from .serializers import ExperimentSerializer
from .paginations import ExperimentPagination


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ExperimentPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'status']
    ordering_fields = ['start_date', 'end_date', 'title']
