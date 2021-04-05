from rest_framework.response import Response
from rest_framework import  (
    viewsets, 
    status, 
    permissions
)
from apps.transaction.models import Transaction, TransactionType
from apps.transaction.serializers import TransactionSerializer, TransactionTypeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.users.models import User
from apps.room.models import Room
from rest_framework.decorators import action

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    """ Transaction ViewSet"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    permission_classes_by_action = {
        'create': [IsAuthenticated], 
        'list': [IsAdminUser],
        }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea una transaccion donde un usuario envía dinero a otro usuario"""
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():    
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        transaction = serializer.save()
        user = self.request.user #usuario que envía
        transaction.userTransmitter = user
        transaction.save()
        user2 = transaction.userReceiver #usuario que recibe
        amount = transaction.amount 

        user.amount -= amount 
        user2.amount += amount
    
        user.save()
        user2.save()

        return transaction

    @action(methods=['post'], detail=True, permission_classes=[IsAdminUser]) 
    def cobrar(self, request, pk=None):
        """ Método que permite al banquero cobrar a un usuario.  
        Nota: solo el usuario banquero tiene acceso a este método."""
        banquero = self.request.user
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(): 
            transaction = serializer.save(userReceiver=banquero)
            jugador = serializer.validated_data['userTransmitter']
            amount = serializer.validated_data['amount']

            banquero.amount += amount
            jugador.amount -= amount
            banquero.save()
            jugador.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """ Lista todas las transacciones que han hecho los usuarios de la sala"""
        banquero = self.request.user
        room = Room.objects.get(userBanker=banquero.id)
        self.queryset = Transaction.objects.filter(userTransmitter__room__idRoom__exact=room.idRoom).order_by('-creationTime')
        serializer = TransactionSerializer(self.queryset, many=True)
        return Response(serializer.data)



    @action(methods=['post'], detail=True, permission_classes=[IsAdminUser])
    def pass_go(self, request, pk=None):
        """ Método que permite al banquero dar pass go ($200) automáticamente a un usuario
        Nota: solo el usuario banquero tiene acceso a este método."""
        banquero = self.request.user
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(userTransmitter=banquero, amount=200)
            jugador = serializer.validated_data['userReceiver']
            jugador.amount += 200
            jugador.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST)
        
class TransactionTypeViewSet(viewsets.ModelViewSet):
    """ Transaction ViewSet"""
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [permissions.AllowAny,]

