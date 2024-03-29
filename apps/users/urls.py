from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet, UserTypeViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'users-type', UserTypeViewSet, basename='user-type')

urlpatterns = [
    path('',include(router.urls)),
]