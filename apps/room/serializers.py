from rest_framework import serializers
from apps.room.models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Room serializer"""
    class Meta:
        model = Room
        fields = ['idRoom','time','status']