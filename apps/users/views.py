from rest_framework.response import Response
from rest_framework import (
    viewsets, 
    status, 
    permissions
)
from apps.users.models import User, UserType 
from apps.room.models import Room
from apps.users.serializers import (
    UserSerializer, 
    UserTypeSerializer, 
    UserListSerializer
)
from apps.transaction.serializers import TransactionSerializer
import shortuuid
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
import math 
from rest_framework.decorators import action

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """User Viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes_by_action = {
        'create': [AllowAny], 
        'list': [IsAuthenticated],
        }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un usuario jugador que solicita entrar en una sala.
        Devuelve el token y los datos del usuario."""
        self.permission_classes = [permissions.AllowAny, ]
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idr = serializer.validated_data['room']
        room = Room.objects.get(idRoom=idr)
        if room.limit < 5:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            token, created = Token.objects.get_or_create(user=serializer.instance)
            data={
                'access_token':token.key,
                'user': serializer.data
            }
            print(request.META)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            mensaje={
                'info': 'La sala ya está llena.',
            }
            return Response(mensaje)

    def perform_create(self, serializer):
        user = serializer.save()
        room = Room.objects.get(idRoom=user.room)
        room.limit +=1
        room.save()
        ut = UserType.objects.get(idUserType="2")
        user.userType = ut 
        user.amount = "1000"
        user.save()
        return user

    def list(self, request):
        """Lista los usuarios según el tipo de usuario:
        Banquero: se muestran los montos exactos de los jugadores
        Jugadores: se muestran los montos aproximados de los jugadores"""
        user = self.request.user
        if user.userType.name == 'Banquero':
            self.queryset = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).order_by('id')
            list_amounts = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).values_list('amount',flat=True).order_by('id')
            serializer = UserListSerializer(self.queryset, many=True)
            data={
                'users':serializer.data,
                'amounts':list_amounts
            }
            #print(serializer.data)
        else:
            self.queryset = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).exclude(userType__name='Banquero').order_by('id')
            list_amounts = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).exclude(userType__name='Banquero').values_list('amount',flat=True).order_by('id')

            def round_down(x):
                return int(math.floor(x / 100.0)) * 100

            new_amounts=[]
            for list in list_amounts:
                a = round_down(list)
                new_amounts.append(a)       
            serializer = UserListSerializer(self.queryset, many=True)
            data={
                'users': serializer.data,
                'round_amounts': new_amounts
            }
            #print(serializer.data)
        return Response(data)
        

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def solicitar_bancarrota(self, request, pk=None):
        """Un jugador solicita bancarrota y transfiere 
        todo su dinero al jugador que lo provocó """
        user1 = self.request.user #usuario que envía
        user1.status = 'I'
        user1.save()
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(userTransmitter=user1, amount=user1.amount)
            amount = user1.amount
            user2 = transaction.userReceiver #usuario que recibe

            user1.amount = 0
            user2.amount +=amount

            user1.save()
            user2.save()
            mensaje={
                'info':'La transacción se ha realizado con éxito.'
            }
            return Response(mensaje, status=status.HTTP_200_OK)
        else:
            return Response({"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def resumen_partida(self, request):
        """ Muestra una lista de los jugadores con los saldos finales de cada uno"""
        user = self.request.user
        self.queryset = User.objects.all().filter(room=user.room).exclude(userType__name='Banquero').order_by('-amount')
        list_amounts = User.objects.all().filter(room=user.room).exclude(userType__name='Banquero').values_list('amount',flat=True).order_by('-amount')
        serializer = UserSerializer(self.queryset, many=True)
        data={
            'users':serializer.data,
            'amounts':list_amounts,
            'info': 'Partida finalizada.'
        }
        return Response(data, status=status.HTTP_200_OK)


class UserTypeViewSet(viewsets.ModelViewSet):
    """ User Type viewset"""
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [permissions.AllowAny, ]
            


