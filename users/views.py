from django.shortcuts import get_object_or_404
from .models import UserProfile, CustomUser
from .serializers import UserProfileSerializer, CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .permissions import IsOwnerOfProfile


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Registration successful."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfProfile]

    def get_object(self):
        return self.request.user.profile


class ProfileByIdView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(UserProfile, user__id=user_id)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(CustomUser, id=user_id)

    if user == target_user:
        return Response({"message": "You cannot follow/unfollow yourself!"}, status=status.HTTP_400_BAD_REQUEST)

    profile = user.profile
    if target_user in profile.following.all():
        profile.following.remove(target_user)
        return Response({"message": "Unfollowed successfully!"})
    else:
        profile.following.add(target_user)
        return Response({"message": "Followed successfully!"})




class BaseFollowListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    relation = None  # "followers" or "following"

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(UserProfile, user=user)

        if self.relation == 'followers':
            data = UserProfile.objects.filter(following=user)
        else:
            data = profile.following.all()

        serializer = UserProfileSerializer(data, many=True)
        return Response(serializer.data)


class FollowersListView(BaseFollowListView):
    relation = 'followers'


class FollowingListView(BaseFollowListView):
    relation = 'following'



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
