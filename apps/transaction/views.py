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
from rest_framework.decorators import action

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    """ Transaction ViewSet"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """Crea una transaccion donde un usuario envía dinero a otro usuario"""
        self.permission_classes = [permissions.IsAuthenticated,]
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated]) #recordar cambiar a IsAdminUser
    def cobrar(self, request, pk=None):
        """ Método que permite al banquero cobrar a un usuario  """
        banquero = self.request.user
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(): 
            transaction = serializer.save(userReceiver=banquero)
            jugador = serializer.validated_data['userTransmitter']
            amount = serializer.validated_data['amount']
            print(banquero.amount)
            print(jugador.amount)

            banquero.amount += amount
            jugador.amount -= amount
            banquero.save()
            jugador.save()

            print(serializer.data)
            print(amount)
            print(banquero.amount)
            print(jugador.amount)

            return Response(transaction, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(methods=['post'], detail=True, permission_classes=[IsAdminUser])
    def pass_go(self, request, pk=None):
        """ Método que permite al banquero dar pass go ($200) automáticamente a un usuario"""
        banquero = self.request.user
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(userTransmitter=banquero, amount=200)
            print(serializer.data)
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

