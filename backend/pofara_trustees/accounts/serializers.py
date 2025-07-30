"""
Serializers for the accounts app.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 
            'last_name', 'phone_number'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            **validated_data
        )
        user.set_password(password)
        user.terms_accepted = True  # Assume terms are accepted during registration
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'role', 'status', 'email_verified', 'phone_verified',
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'role', 'status', 'email_verified', 'phone_verified',
            'is_verified', 'created_at', 'updated_at'
        ]


class AuthResponseSerializer(serializers.Serializer):
    """Serializer for authentication response."""
    
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Try to get user by email
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials.')
            
            # Authenticate user
            user = authenticate(username=user.username, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.can_login():
                raise serializers.ValidationError('Account is not active or locked.')
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Must include email and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'avatar', 'date_of_birth', 'gender', 'bio',
            'country', 'city', 'address', 'postal_code',
            'country_of_origin', 'languages_spoken',
            'timezone', 'language_preference', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value 