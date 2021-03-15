from rest_framework import  (
    viewsets, 
    status, 
    permissions
)
from rest_framework.permissions import IsAuthenticated
from apps.room.models import Room
from apps.users.models import User
from apps.room.serializers import RoomSerializer

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    """Room viewset"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny, ]

