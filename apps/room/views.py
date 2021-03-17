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

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    """Room viewset"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    permission_classes_by_action = {
        'create': [AllowAny], 
        'list': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        """ Crea la sala y el usuario banquero.
        Devuelve el código de la sala y el token del usuario. """
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

    def destroy(self, request, *args, **kwargs):
        """Después del resumen de partida, se eliminan los datos de la DB """
        instance = self.get_object()
        banquero = instance.userBanker
        self.perform_destroy(instance)
        banquero.delete()
        mensaje={
            'info':'Datos eliminados.'
        }
        return Response(mensaje, status=status.HTTP_204_NO_CONTENT) 
