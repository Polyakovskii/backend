from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from trading_app.serializers import UserSerializer, ListUserSerializer, UpdateUserSerializer
from trading_app.permissions import IsOwner
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
