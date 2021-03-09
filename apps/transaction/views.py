from rest_framework import viewsets, status
from apps.transaction.models import Transaction
from apps.transaction.serializers import TransactionSerializer

# Create your views here.
class TransactionViewSer(viewsets.ModelViewSet):
    """ Transaction ViewSet"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
