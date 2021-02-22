from django.db import models
import shortuuid 
from datetime import datetime

# Create your models here.
class Room(models.Model):
    """Modelo de la sala"""
    su = shortuuid.ShortUUID().random(length=8)
    idRoom = models.CharField(max_length=10, default=su, primary_key=True)
    time = models.DateTimeField(default=datetime.now)
    STATUS =( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.idRoom

    class Meta: 
        db_table = "Room"