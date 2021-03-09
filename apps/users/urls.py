from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet, UserTypeViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'usersType', UserTypeViewSet, basename='userType')

urlpatterns = [
    path('',include(router.urls)),
]