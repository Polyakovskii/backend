"""
All main Serializers
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from trading_app.models import Currency, Item, WatchList, Inventory, Offer, Trade
from trading_app.enums import TransactionTypeEnum


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


class InventorySerializer(serializers.ModelSerializer):
    """
    Inventory serializer
    """
    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    """
    Default offer serializer
    """
    item = ItemSerializer()
    user = ListUserSerializer()

    class Meta:
        model = Offer
        fields = "__all__"


class CreateOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for offer creation
    """
    class Meta:
        model = Offer
        fields = ('item', 'entry_quantity', 'order_type', 'transaction_type', 'price')

    @staticmethod
    def validate(attrs):
        if attrs['entry_quantity'] <= 0:
            raise serializers.ValidationError("Quantity should be positive number")
        return attrs

    def create(self, validated_data):

        user = self.context['request'].user

        if validated_data['transaction_type'] == TransactionTypeEnum.sale.value:
            try:
                item = user.inventory.get(item=validated_data.get('item'))
                if item.quantity - item.reserved_quantity < validated_data.get('entry_quantity'):
                    raise serializers.ValidationError(
                        "You don't have enough not reserved items of that type in your inventory"
                    )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    "You don't have items of that type in your inventory"
                )
            item.reserved_quantity += validated_data.get('entry_quantity')
            item.save()

        validated_data['user'] = user
        validated_data['quantity'] = validated_data['entry_quantity']

        offer = Offer(**validated_data)
        offer.save()
        return offer


class TradeSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    seller = ListUserSerializer()
    seller_offer = OfferSerializer()
    buyer = ListUserSerializer()
    buyer_offer = OfferSerializer()

    class Meta:
        model = Trade
        fields = "__all__"
