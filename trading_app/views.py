from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from trading_app.serializers import (
    UserSerializer,
    ListUserSerializer,
    UpdateUserSerializer,
    CurrencySerializer,
    WatchListSerializer,
    CreateWatchListSerializer
)
from trading_app.permissions import IsOwner
from trading_app.models import Currency, WatchList
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

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self, ):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'update':
            return [IsOwner()]
        return [permissions.IsAuthenticated()]


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
