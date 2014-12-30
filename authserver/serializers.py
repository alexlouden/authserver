from rest_framework import serializers
from authserver.models import User, Role, APIKey


class JSONDataField(serializers.Field):
    def to_representation(self, obj):
        return obj.data


class UserSerializer(serializers.ModelSerializer):

    roles = serializers.StringRelatedField(many=True)
    data = JSONDataField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'password',
            'roles',
            'data'
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'data',
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id', )


class KeySerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = APIKey
        fields = (
            'key',
            'secret',
            'user'
        )
        read_only_fields = (
            'user',
        )


class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=100)


class SecretSerializer(serializers.Serializer):

    secret = serializers.CharField(max_length=100)
