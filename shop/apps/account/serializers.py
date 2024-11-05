"""
This module contains serializers for the CustomUser model,
handling account management processes like registration, login, and password management.
"""

from rest_framework import serializers
from apps.account.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model to include all fields."""

    class Meta:
        model = CustomUser
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with mobile number validation."""

    def validate_mobile_number(self, mobile_number):
        """
        Validate mobile number format and length.
        The mobile number should be 11 characters and start with '09'.
        """
        if len(mobile_number) != 11:
            raise serializers.ValidationError(
                'The length of mobile_number is not valid'
            )
        if not mobile_number.startswith('09'):
            raise serializers.ValidationError(
                'The format is not valid; mobile number should start with "09".'
            )
        return mobile_number

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password']


class ActiveCodeSerializer(serializers.ModelSerializer):
    """Serializer for validating active codes during user activation."""

    class Meta:
        model = CustomUser
        fields = ['active_code']


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for user login with mobile number and password validation."""

    def validate_mobile_number(self, mobile_number):
        """
        Validate mobile number format and length.
        The mobile number should be 11 characters and start with '09'.
        """
        if len(mobile_number) != 11:
            raise serializers.ValidationError(
                'The length of mobile_number is not valid'
            )
        if not mobile_number.startswith('09'):
            raise serializers.ValidationError(
                'The format is not valid; mobile number should start with "09".'
            )
        return mobile_number

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password']


class RememberPasswordSerializer(serializers.ModelSerializer):
    """Serializer for resetting password by validating mobile number."""

    def validate_mobile_number(self, mobile_number):
        """
        Validate mobile number format and length.
        The mobile number should be 11 characters and start with '09'.
        """
        if len(mobile_number) != 11:
            raise serializers.ValidationError(
                'The length of mobile_number is not valid'
            )
        if not mobile_number.startswith('09'):
            raise serializers.ValidationError(
                'The format is not valid; mobile number should start with "09".'
            )
        return mobile_number

    class Meta:
        model = CustomUser
        fields = ['mobile_number']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for password change with confirmation field."""
    re_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['password', 're_password']
