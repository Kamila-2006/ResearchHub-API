from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profiles/me/', views.CurrentUserProfileView.as_view(), name='profile-me'),
    path('profiles/<int:user_id>/', views.ProfileByIdView.as_view(), name='profile-detail'),
    path('profiles/<int:user_id>/follow/', views.toggle_follow, name='profile-follow'),
    path('profiles/<int:user_id>/unfollow/', views.toggle_follow, name='profile-unfollow'),
    path('profiles/<int:user_id>/followers/', views.FollowersListView.as_view(), name='profile-followers'),
    path('profiles/<int:user_id>/following/', views.FollowingListView.as_view(), name='profile-following'),
    path('users/me/', views.CurrentUserView.as_view(), name='user-me'),
    path('users/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
]
