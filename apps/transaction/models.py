from django.db import models
from apps.users.models import User
from datetime import datetime

# Create your models here.
class TransactionType(models.Model):
    """Modelo del tipo de transaccion"""
    idTrType = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=15)
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.name

    class Meta: 
        db_table = "TransactionType"


class Transaction(models.Model):
    """Modelo de Transaccion"""
    idTransaction = models.CharField(max_length=15, primary_key=True)
    TnType = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='id_tn_type')
    userReceiver = models.ForeignKey(User,on_delete=models.CASCADE,
        related_name='user_receiver')
    userTransmitter = models.ForeignKey(User,on_delete=models.CASCADE, 
        related_name='user_transmitter')
    amount = models.IntegerField()
    creationTime = models.DateTimeField(default=datetime.now)
    concept = models.CharField(max_length=80, blank=True, null=True)
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.idTransaction + ' / ' + self.userReceiver + ' / ' + self.userTransmitter

    class Meta: 
        db_table = "Transaction"
