from django.contrib import admin
from apps.transaccion.models import Transaccion, TransactionType

# Register your models here.
admin.site.register(TransactionType)
admin.site.register(Transaccion)
