from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, MemberViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'members', MemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
]
