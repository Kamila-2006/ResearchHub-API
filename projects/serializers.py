from rest_framework import serializers
from .models import Project, ProjectMember
from users.serializers import CustomUserSerializer


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role', 'joined_at', 'is_active']


class ProjectSerializer(serializers.ModelSerializer):
    members = ProjectMemberSerializer(many=True, read_only=True)
    principal_investigator = CustomUserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'short_description', 'description',
            'start_date', 'end_date', 'status', 'visibility',
            'funding_source', 'funding_amount', 'funding_currency',
            'group', 'principal_investigator', 'members', 'is_active',
            'created_at', 'updated_at'
        ]
