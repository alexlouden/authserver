from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route  # list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authserver.models import User, Role, APIKey
from authserver.serializers import (
    UserSerializer,
    RoleSerializer,
    KeySerializer,
    OnlyKeySerializer,
    PasswordSerializer,
    SecretSerializer
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()

        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.data['password'])
        user.save()
        return Response({'status': 'password set'})

    @detail_route(methods=['post'])
    def check_password(self, request, pk=None):
        user = self.get_object()

        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        correct_pass = user.check_password(serializer.validated_data['password'])
        return Response(correct_pass)

    @detail_route()
    def roles(self, request, pk=None):
        user = self.get_object()
        serializer = RoleSerializer(user.roles, many=True)
        return Response(serializer.data)

    @detail_route()
    def keys(self, request, pk=None):
        user = self.get_object()
        serializer = OnlyKeySerializer(user.keys, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def create_key(self, request, pk=None):
        user = self.get_object()

        serializer = KeySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # It's valid, now create object
        key = serializer.validated_data['key']
        secret = serializer.validated_data['secret']
        APIKey.objects.create(user=user, key=key, secret=secret)

        return Response({'status': 'key created'})

    @detail_route(methods=['post'])
    def check_role(self, request, pk=None):

        user = self.get_object()

        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        role = serializer.validated_data['name']

        return Response(user.has_role(role))

    @detail_route(methods=['post'])
    def add_role(self, request, pk=None):

        user = self.get_object()

        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        role = serializer.validated_data['name']

        return Response(user.add_role(role))

    @detail_route(methods=['post'])
    def remove_role(self, request, pk=None):

        user = self.get_object()

        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        role = serializer.validated_data['name']

        return Response(user.remove_role(role))


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'name'


class KeyViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        GenericViewSet):

    lookup_field = 'key'
    queryset = APIKey.objects.all()
    serializer_class = KeySerializer

    @detail_route(methods=['post'])
    def check_secret(self, request, key=None):

        key = self.get_object()

        serializer = SecretSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        secret = serializer.validated_data['secret']

        if key.secret != secret:
            return Response(
                {status: False},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = KeySerializer(key)
        return Response(serializer.data)
