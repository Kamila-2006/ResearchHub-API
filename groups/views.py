from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from .models import Group, Member
from .serializers import GroupSerializer, MemberSerializer
from .pagination import GroupPagination, MemberPagination
from .permissions import IsGroupLeaderOrReadOnly


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsGroupLeaderOrReadOnly]
    pagination_class = GroupPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'institution']
    ordering_fields = ['name', 'institution']

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsGroupLeaderOrReadOnly]
    pagination_class = MemberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__full_name', 'role']
    ordering_fields = ['joined_at', 'role']

    def perform_create(self, serializer):
        group = serializer.validated_data.get('group')
        user = self.request.user
        if not group.members.filter(user=user, role='leader', is_active=True).exists():
            raise PermissionDenied("Only group leaders can add members.")
        serializer.save()
