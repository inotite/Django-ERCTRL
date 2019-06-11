from rest_framework import serializers
from erm_room.models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'room_name', 'num_clues')


class UserRoomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_name']


class TabletRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ()
