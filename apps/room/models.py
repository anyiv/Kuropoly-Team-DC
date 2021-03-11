from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    """Modelo de la sala"""
    idRoom = models.CharField(max_length=10, primary_key=True)
    time = models.DateTimeField(default=datetime.now)
    limit = models.IntegerField(default='0')
    userBanker = models.ForeignKey("users.User", 
    on_delete=models.CASCADE,
    related_name='id_banker',
    blank=True, null=True)
    STATUS =( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.idRoom

    class Meta: 
        db_table = "Room"