from .models import CustomUser, UserProfile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password



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



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name',
            'institution', 'department', 'position', 'orcid_id'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
