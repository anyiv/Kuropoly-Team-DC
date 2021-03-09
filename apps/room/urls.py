from rest_framework.routers import DefaultRouter
from apps.room.views import RoomViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('',include(router.urls)),
]
