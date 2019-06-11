from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .serializers import UserSerializer
from .permissions import IsAdministrator


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdministrator,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def to_user_room_json(self):
        user = self.get_object()
        user_rooms = user.user_rooms.all()
        user_room_json = {
            'user_id': user.id,
            'user_email': user.email,
            'user_rooms': {}
        }
        for room in user_rooms:
            user_room_json['user_rooms']['room_id'] = room.id
            user_room_json['user_rooms']['room_name'] = room.room_name

        return user_room_json

    @detail_route()
    def rooms(self, request, pk=None):
        """
        Returns a list of all the rooms that the given
        user belongs to.
        """
        user_room_json = self.to_user_room_json()
        return Response(user_room_json)


