from django.db import models
from apps.users.models import User
from datetime import datetime
from django.contrib import admin

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
    TnType = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='id_tn_type', unique = True)
    userReceiver = models.ForeignKey(User,on_delete=models.CASCADE,
        related_name='user_receiver', blank=True, null=True, unique = True)
    userTransmitter = models.ForeignKey(User,on_delete=models.CASCADE, 
        related_name='user_transmitter', blank=True, null=True, unique = True)
    amount = models.IntegerField(blank=True, null=True)
    creationTime = models.DateTimeField(default=datetime.now)
    concept = models.CharField(max_length=80, blank=True, null=True)
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.id

    class Meta: 
        db_table = "Transaction"

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'userReceiver', 'userTransmitter', 'amount' )
