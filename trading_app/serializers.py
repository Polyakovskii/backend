"""
All main Serializers
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from trading_app.models import Currency


class UserSerializer(serializers.ModelSerializer):
    """
    Default User serializer
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating User
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}, }


class ListUserSerializer(serializers.ModelSerializer):
    """
    Serializer for .list() action
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',)


class CurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for Currency
    """
    class Meta:
        model = Currency
        fields = "__all__"
