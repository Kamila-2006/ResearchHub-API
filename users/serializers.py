from .models import CustomUser, UserProfile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.exceptions import TokenExpiredOrInvalid
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
import uuid





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

        # Token yaratish
        token = str(uuid.uuid4())
        email = validated_data['email']

        # Foydalanuvchi datasi token verify bo‘lishi uchun saqlanadi
        user_data = validated_data.copy()
        user_data['password'] = password

        # Cache ga saqlash (token -> email), (email -> (token, user_data))
        cache.set(token, email, timeout=3600)  # 1 soat
        cache.set(email, (token, user_data), timeout=3600)

        # Email yuborish
        send_mail(
            subject="Verify your email",
            message=f"Use this token to verify your email: {token}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return validated_data  # or return something neutral




class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if not value:
            raise serializers.ValidationError("Token is required.")
        return value

    def save(self, **kwargs):
        token = self.validated_data['token']
        email = cache.get(token)
        if not email:
            raise TokenExpiredOrInvalid()

        cached_data = cache.get(email)
        if not cached_data:
            raise TokenExpiredOrInvalid()

        cached_token, user_data = cached_data
        if cached_token != token:
            raise TokenExpiredOrInvalid()

        user = CustomUser.objects.create_user(**user_data)

        cache.delete(token)
        cache.delete(email)

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def save(self):
        token = self.validated_data['token']
        email = cache.get(token)
        if not email:
            raise serializers.ValidationError("Token is invalid or has expired.")

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User does not exist.")

        user.set_password(self.validated_data['password'])
        user.save()

        # Tokenni o'chirib tashlaymiz
        cache.delete(token)

        return user