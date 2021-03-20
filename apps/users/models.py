from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.room.models import Room
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    username = models.CharField(max_length=15, unique=True, default=None)
    amount = models.IntegerField(blank=True,null=True)
    avatar = models.CharField(max_length=10,blank=True,null=True)
    STATUS = ( 
        ('A','Active'),
        ('I','Inactive'),
    )
    status = models.CharField(max_length=1,choices=STATUS, default='A')
    first_name = None
    last_name = None
    last_login = None
    date_joined = None 
    
    def __str__(self):
        return self.username

    class Meta: 
        db_table = "User"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
