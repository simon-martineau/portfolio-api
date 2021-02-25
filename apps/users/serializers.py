from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers

from apps.users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data: dict):
        user = User(**data)
        password = data.get('password')
        errors = {}
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)

    def create(self, validated_data: dict):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail')

    class Meta:
        model = User
        fields = ['id', 'email', 'groups', 'url']
