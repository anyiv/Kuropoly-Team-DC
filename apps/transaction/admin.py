from django.contrib import admin
from apps.transaction.models import Transaction, TransactionType

# Register your models here.
admin.site.register(TransactionType)
admin.site.register(
    Transaction,
    list_display=["id","userReceiver","userTransmitter"]
    )
