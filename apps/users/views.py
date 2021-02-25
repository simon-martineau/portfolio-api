from rest_framework import generics, viewsets, mixins, exceptions
from rest_framework import permissions

from apps.users.serializers import RegisterUserSerializer, UserSerializer
from apps.users.models import User


class RegisterUserView(generics.CreateAPIView):
    """View to create a user"""
    serializer_class = RegisterUserSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Viewset for the users endpoint"""
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def permission_denied(self, request, message=None, code=None):
        """We override this so we can replace 403s by 404s to not give away an object's existence"""
        if self.action in ('update', 'partial_update', 'destroy', 'retrieve'):
            raise exceptions.NotFound(detail=message, code=code)
        elif request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        else:
            raise exceptions.PermissionDenied(detail=message, code=code)
