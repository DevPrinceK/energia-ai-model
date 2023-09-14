from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate


from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'id')  # noqa


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
        )
        return user
