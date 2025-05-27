from rest_framework import serializers
from .models import Project, ProjectMember
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    user_detail = CustomUserSerializer(source='user', read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'user_detail', 'project', 'role', 'joined_at', 'is_active']
        extra_kwargs = {'joined_at': {'read_only': True}, 'is_active': {'default': True}}


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
