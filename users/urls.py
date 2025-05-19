from django.urls import path
from .views import (
    UserProfileDetailView, MyProfileView, FollowUserView, UnfollowUserView,
    FollowersListView, FollowingListView,
    CurrentUserView, UserDetailView,
)

urlpatterns = [
    path('profiles/me/', MyProfileView.as_view(), name='my-profile'),
    path('profiles/<int:user__id>/', UserProfileDetailView.as_view(), name='user-profile'),
    path('profiles/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('profiles/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('profiles/<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('profiles/<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
    path('users/me/', CurrentUserView.as_view(), name='user-me'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]
