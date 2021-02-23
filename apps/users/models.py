from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.room.models import Room


class UserType(models.Model):
    """Modelo Tipo de Usuario"""
    idUserType = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=15)
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')

    def __str__(self):
        return self.name

    class Meta: 
        db_table = "UserType"

class User(AbstractUser):
    """Modelo usuario"""
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE,
     blank=True, null=True,
     related_name='id_user_type')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=15, unique=True)
    amount = models.IntegerField()
    avatar = models.ImageField(upload_to='pictures/', default='pictures/default.jpg')
    first_name = None
    last_name = None
    email = None
    last_login = None 
    is_staff = None
    is_superuser = None
    USERNAME_FIELD = 'name' 
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')
    def __str__(self):
        return self.name

    class Meta: 
        db_table = "User"



