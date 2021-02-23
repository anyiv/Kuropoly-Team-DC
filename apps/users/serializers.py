from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['userType',
            'room', 'name',
            'amount','avatar',
            'status'
        ]