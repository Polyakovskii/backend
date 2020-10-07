"""
All main Serializers
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from trading_app.models import Currency, Item, WatchList


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


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item
    """
    currency = CurrencySerializer()

    class Meta:
        model = Item
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    """
    Default serializer for WatchList
    """
    item = ItemSerializer()

    class Meta:
        model = WatchList
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}


class CreateWatchListSerializer(serializers.ModelSerializer):
    """
    Serializer for creating WatchList
    """
    class Meta:
        model = WatchList
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        watchlist = WatchList(user=user, **validated_data)
        watchlist.save()
        return watchlist
