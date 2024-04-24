from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_rentier = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name',
                  'is_active', 'is_verified', "is_rentier", 'is_staff']

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        validated_data["password"] = hashed_password
        user = super(UserSerializer, self).create(validated_data)
        return user


class UserFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]


class UserUpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number"]


class UserPasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
