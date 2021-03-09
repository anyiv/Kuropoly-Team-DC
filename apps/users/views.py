from rest_framework import viewsets, status
from apps.users.models import User, UserType 
from apps.room.models import Room
from apps.users.serializers import UserSerializer, UserTypeSerializer
import shortuuid

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """User Viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserTypeViewSet(viewsets.ModelViewSet):
    """ User Type viewset"""
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
            


