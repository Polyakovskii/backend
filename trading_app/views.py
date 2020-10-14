from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from django_filters import rest_framework as filters
from trading_app.serializers import (
    UserSerializer,
    ListUserSerializer,
    UpdateUserSerializer,
    CurrencySerializer,
    WatchListSerializer,
    CreateWatchListSerializer,
    InventorySerializer,
    OfferSerializer,
    CreateOfferSerializer,
    TradeSerializer
)
from trading_app.permissions import IsOwnerOrAuthenticatedReadOnly
from trading_app.models import Currency, WatchList, Inventory, Offer, Trade
from trading_app.filters import OfferFilter, TradeFilter, InventoryFilter
# Create your views here.


class UserView(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
):
    """
    User view.
    """
    queryset = User.objects.all()
    default_serializer_class = UserSerializer
    serializer_classes = {
        "list": ListUserSerializer,
        "create": UserSerializer,
        "retrieve": UserSerializer,
        "update": UpdateUserSerializer,
    }

    permission_classes = [IsOwnerOrAuthenticatedReadOnly]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class CurrencyView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    """
    CurrencyView
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class WatchListView(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin
):
    """
    WatchList View
    """
    default_serializer_class = WatchListSerializer
    serializer_classes = {
        'list': WatchListSerializer,
        'retrieve': WatchListSerializer,
        'create': CreateWatchListSerializer
    }
    lookup_field = "item"

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class InventoryView(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin
):
    """
    Inventory view
    """
    serializer_class = InventorySerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = InventoryFilter

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)


class OfferView(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin
):
    """
    Offer view
    """
    default_serializer_class = OfferSerializer
    serializer_classes = {
        'list': OfferSerializer,
        'create': CreateOfferSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = OfferFilter

    def get_queryset(self):
        return Offer.objects.filter(is_active=True)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class TradeView(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin
):
    """
    Trade View
    """
    serializer_class = TradeSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TradeFilter

    def get_queryset(self):
        return Trade.objects.filter(Q(buyer=self.request.user) | Q(seller=self.request.user))
