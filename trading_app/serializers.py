from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Default User serializer
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ListUserSerializer(serializers.ModelSerializer):
    """
    Serializer fo .list() action
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)
