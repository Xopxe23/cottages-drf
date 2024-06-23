import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User, VerifyCode


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_rentier = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name',
                  'is_active', 'is_verified', "is_rentier", 'is_staff']


class UserFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]


class UserUpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number"]


class VerifyCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = VerifyCode
        fields = ["email", "code"]

    @staticmethod
    def validate_code(value):
        if not re.match(r'^[A-Z]{6}$', value):
            raise serializers.ValidationError("Code must be 6 uppercase letters")
        return value
