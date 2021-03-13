from rest_framework.response import Response
from rest_framework import viewsets, status
from apps.users.models import User, UserType 
from apps.room.models import Room
from apps.users.serializers import UserSerializer, UserTypeSerializer
import shortuuid
from rest_framework.authtoken.models import Token

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """User Viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        data={
            'access_token':token.key,
            'user': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        room = Room.objects.get(idRoom=user.room)
        room.limit +=1
        room.save()
        ut = UserType.objects.get(idUserType="2")
        user.userType = ut 
        user.amount = "1000"
        user.save()
        return user

    def list(self, request):
        # user = request.user
        # if user.userType == "2":
        #     self.queryset = User.objects.all().filter(status='A')
        #     self.context['amounts'] = User.objects.all().filter(status='A').values('amount')
            
        #     serializer = UserSerializer(self.queryset, many=True)
        # else:
        self.queryset = User.objects.all().filter(status='A').exclude(userType='1')
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)



class UserTypeViewSet(viewsets.ModelViewSet):
    """ User Type viewset"""
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
            


