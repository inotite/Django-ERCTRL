from rest_framework import serializers
from erm_room.models import GameRecord


class GameRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameRecord
        fields = ('id', 'team_name')
