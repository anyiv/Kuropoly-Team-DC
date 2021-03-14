from rest_framework import serializers
from rest_framework.authtoken.models import Token
from apps.room.models import Room
from apps.users.models import User, UserType
from apps.users.serializers import UserRoomSerializer
import shortuuid

class RoomSerializer(serializers.ModelSerializer):
    """Room serializer"""
    userBanker = UserRoomSerializer()
    class Meta:
        model = Room
        fields = [
            'userBanker',
            'status',
            ]

    def create(self, validated_data):
        """Crea la sala y el banquero de la sala"""
        users_data = validated_data.pop('userBanker')
        su = shortuuid.ShortUUID().random(length=8)
        ut = UserType.objects.get(idUserType="1")
        user = User.objects.create(userType = ut,
            amount=100000,
            **users_data)
        room = Room.objects.create(idRoom=su,
            userBanker = user,
            **validated_data)
        room.limit = 1
        room.save()
        return su, room