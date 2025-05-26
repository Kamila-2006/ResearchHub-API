from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FindingViewSet

router = DefaultRouter()
router.register(r'findings', FindingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
