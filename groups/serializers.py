from rest_framework import serializers
from .models import Group, Member
from users.models import CustomUser

class MemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = Member
        fields = ['id', 'user', 'group', 'role', 'joined_at', 'is_active']

class GroupSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'institution', 'department', 'website', 'logo', 'members']
