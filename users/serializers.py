from rest_framework import serializers
from .models import CustomUser, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    projects_count = serializers.ReadOnlyField()
    publications_count = serializers.ReadOnlyField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'research_interests', 'avatar', 'website', 'google_scholar', 'researchgate',
            'linkedin', 'twitter', 'following',
            'followers_count', 'following_count', 'projects_count', 'publications_count', 'projects'
        ]
        read_only_fields = ['followers_count', 'following_count', 'projects_count', 'publications_count', 'projects']

    def get_projects(self, obj):
        projects = obj.projects
        return [project.id for project in projects]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'institution', 'department', 'position', 'orcid_id',
            'is_verified', 'date_joined', 'role', 'citation_count', 'h_index', 'profile_url', 'profile'
        ]
        read_only_fields = ['date_joined']

