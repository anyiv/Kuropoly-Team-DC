from rest_framework import serializers
from apps.users.models import User, UserType

class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['room', 
            'username',
            'avatar'
        ]


class UserRoomSerializer(serializers.ModelSerializer):
    """User room serializer"""
    class Meta:
        model = User
        fields = [
            'username',
            'avatar'
        ]


class UserTypeSerializer(serializers.ModelSerializer):
    """User Type serializer"""

    class Meta:
        model = UserType
        fields = '__all__'