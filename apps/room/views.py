from django.shortcuts import render
from rest_framework import viewsets, status
from apps.room.models import Room
from apps.room.serializers import RoomSerializer

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    """Room view set"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

