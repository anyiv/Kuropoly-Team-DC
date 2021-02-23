from rest_framework import serializers
from apps.transaction.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """ Transaction serializer"""
    class Meta:
        model = Transaction
        fields = '__all__'