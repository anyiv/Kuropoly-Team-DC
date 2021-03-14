from rest_framework.response import Response
from rest_framework import (
    viewsets, 
    status, 
    permissions
)
from apps.users.models import User, UserType 
from apps.room.models import Room
from apps.users.serializers import UserSerializer, UserTypeSerializer
import shortuuid
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import math 
from rest_framework.decorators import action

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """User Viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    
    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.AllowAny, ]
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idr = serializer.validated_data['room']
        print(idr)
        room = Room.objects.all().get(idRoom=idr)
        print(room.limit)
        if room.limit < 5:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            token, created = Token.objects.get_or_create(user=serializer.instance)
            data={
                'access_token':token.key,
                'user': serializer.data
            }
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
        self.permission_classes = [permissions.IsAuthenticated, ]
        
        name = request.user
        user = User.objects.get(username=name)
        print(name,user.userType, user.room, user.id)
        if user.userType.name == 'Banquero' and user.room==None:
            roomBanker = Room.objects.get(userBanker=user.id)
            self.queryset = User.objects.all().filter(status='A',room=roomBanker).exclude(userType='Banquero')
            list_amounts = User.objects.all().filter(status='A',room=roomBanker).values_list('amount',flat=True).order_by('id')
            serializer = UserSerializer(self.queryset, many=True)
            data={
                'users':serializer.data,
                'amounts':list_amounts
            }
            #print(serializer.data)
        else:
            self.queryset = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).order_by('id')
            list_amounts = User.objects.all().filter(status='A',room=user.room).exclude(id=user.id).values_list('amount',flat=True).order_by('id')

            def round_down(x):
                return int(math.floor(x / 100.0)) * 100

            new_amounts=[]
            for list in list_amounts:
                a = round_down(list)
                new_amounts.append(a)       
            serializer = UserSerializer(self.queryset, many=True)
            data={
                'users': serializer.data,
                'round_amounts': new_amounts
            }
            #print(serializer.data)
        return Response(data)
        

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def solicitarBancarrota(self, request, pk):
        return 0



class UserTypeViewSet(viewsets.ModelViewSet):
    """ User Type viewset"""
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
            


