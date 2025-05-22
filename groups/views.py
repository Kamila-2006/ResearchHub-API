from rest_framework import viewsets, permissions, filters
from .models import Group, Member
from .serializers import GroupSerializer, MemberSerializer
from .pagination import GroupPagination, MemberPagination

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GroupPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'institution']
    ordering_fields = ['name', 'institution']

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MemberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__full_name', 'role']
    ordering_fields = ['joined_at', 'role']
