from rest_framework import viewsets, filters
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
