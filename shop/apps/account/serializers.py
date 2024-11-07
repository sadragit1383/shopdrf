from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from apps.account.models import CustomUser

# Validator for mobile numbers to avoid repetitive code
def validate_mobile_number(mobile_number):
    """Validate that the mobile number starts with '09' and is 11 characters."""
    if len(mobile_number) != 11 or not mobile_number.startswith('09'):
        raise serializers.ValidationError(
            'Mobile number should be 11 digits and start with "09".'
        )
    return mobile_number


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model, handling all fields."""

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'is_admin']  # Set fields as read-only if needed


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with mobile number validation and password hashing."""
    mobile_number = serializers.CharField(validators=[validate_mobile_number])

    def create(self, validated_data):
        """Override create method to hash password before saving."""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class ActiveCodeSerializer(serializers.ModelSerializer):
    """Serializer for validating active codes during user activation."""

    class Meta:
        model = CustomUser
        fields = ['active_code']
        extra_kwargs = {'active_code': {'write_only': True}}


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for user login with mobile number and password validation."""
    mobile_number = serializers.CharField(validators=[validate_mobile_number])

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class RememberPasswordSerializer(serializers.ModelSerializer):
    """Serializer for password reset by validating mobile number."""
    mobile_number = serializers.CharField(validators=[validate_mobile_number])

    class Meta:
        model = CustomUser
        fields = ['mobile_number']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for password change with password confirmation."""
    re_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password != re_password:
            raise serializers.ValidationError({'re_password': 'Passwords do not match.'})

        validate_password(password, self.instance)  # Validate against Django's built-in validators

        if self.instance.check_password(password):
            raise serializers.ValidationError({'password': 'New password cannot be the same as the old password.'})

        return attrs

    def update(self, instance, validated_data):
        """Override update to hash password before saving."""
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['password', 're_password']
        extra_kwargs = {'password': {'write_only': True}}
