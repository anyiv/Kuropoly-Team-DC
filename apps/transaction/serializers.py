from rest_framework import serializers
from apps.transaction.models import Transaction, TransactionType

class TransactionSerializer(serializers.ModelSerializer):
    """ Transaction serializer"""
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'TnType',
            'userReceiver',
            'concept',
            'userTransmitter',
        ]

class TransactionTypeSerializer(serializers.ModelSerializer):
    """Transaction type serializer"""
    class Meta:
        model= TransactionType
        fields = [
            'idTrType',
            'name',
        ]
