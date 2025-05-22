from rest_framework import serializers
from .models import Group, Member
from users.serializers import CustomUserSerializer

class MemberSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'role', 'joined_at', 'is_active']

class GroupSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'institution', 'department', 'website', 'logo', 'members']
