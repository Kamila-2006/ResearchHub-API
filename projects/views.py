from rest_framework import viewsets, filters
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from .pagination import ProjectPagination, ProjectMemberPagination
from .permissions import IsProjectPrincipalInvestigatorOrReadOnly, IsProjectMemberPrincipalInvestigatorOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectPrincipalInvestigatorOrReadOnly]
    pagination_class = ProjectPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description', 'description']
    ordering_fields = ['start_date', 'end_date', 'title']


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsProjectMemberPrincipalInvestigatorOrReadOnly]
    pagination_class = ProjectMemberPagination