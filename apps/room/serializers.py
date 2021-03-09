from rest_framework import serializers
from apps.room.models import Room
from apps.users.models import User, UserType
from apps.users.serializers import UserRoomSerializer
import shortuuid

class RoomSerializer(serializers.ModelSerializer):
    """Room serializer"""
    userBanker = UserRoomSerializer()
    class Meta:
        model = Room
        fields = ['userBanker',
        'status',]

    def create(self, validated_data):
        users_data = validated_data.pop('userBanker')
        su = shortuuid.ShortUUID().random(length=8)
        ut = UserType.objects.get(idUserType="1")
        user = User.objects.create(userType = ut,
         **users_data)
        room = Room.objects.create(idRoom=su,
         userBanker = user,
          **validated_data)
        return room