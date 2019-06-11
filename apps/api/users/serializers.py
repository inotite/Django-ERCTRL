from django.contrib.auth.models import User
from rest_framework import serializers
from rest_auth.models import TokenModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email'
                  'username'
                  )


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = TokenModel
        fields = ('key', 'user_id')

    def to_representation(self, value):
        user = User.objects.get(id=value.user_id)
        return({
            'key': value.key,
            'username': user.username,
            'email': user.email,
            'status': 1,
            'msg': "Succesfully logged in",
            'id': user.id
        })
