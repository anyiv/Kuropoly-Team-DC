from rest_framework import  (
    viewsets, 
    status, 
    permissions
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.room.models import Room
from apps.users.models import User
from apps.room.serializers import RoomSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    """Room viewset"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.AllowAny, ]
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        name = list(serializer.data['userBanker'].items())[0][1]
        banquero = User.objects.get(username=name)
        room = serializer.instance
        idroom = room.idRoom
        token, created = Token.objects.get_or_create(user=banquero)
        data={
            'idroom':idroom,
            'access_token':token.key
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
