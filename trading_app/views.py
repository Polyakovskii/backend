from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from trading_app.serializers import UserSerializer, ListUserSerializer
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
        "update": UserSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self, ):
        if self.action == 'post':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
