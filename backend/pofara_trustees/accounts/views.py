"""
Authentication and user management views for the accounts app.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import login
from django.utils import timezone

from .models import User, UserProfile, LoginAttempt
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    AuthResponseSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """Handle user registration with JWT token generation."""
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Update user status to active after successful registration
            user.status = User.Status.ACTIVE
            user.save()
            
            # Log successful registration attempt
            LoginAttempt.objects.create(
                user=user,
                email=user.email,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status=LoginAttempt.Status.SUCCESS
            )
            
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CustomLoginView(APIView):
    """Custom login view with JWT token generation."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.last_login = timezone.now()
            user.last_login_ip = self.get_client_ip(request)
            user.save(update_fields=['failed_login_attempts', 'last_login', 'last_login_ip'])
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Log successful login attempt
            LoginAttempt.objects.create(
                user=user,
                email=user.email,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status=LoginAttempt.Status.SUCCESS
            )
            
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        # Log failed login attempt
        email = request.data.get('email', '')
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                user.failed_login_attempts += 1
                
                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.lock_account()
                else:
                    user.save(update_fields=['failed_login_attempts'])
                    
                LoginAttempt.objects.create(
                    user=user,
                    email=email,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    status=LoginAttempt.Status.FAILED,
                    failure_reason='Invalid credentials'
                )
            except User.DoesNotExist:
                LoginAttempt.objects.create(
                    email=email,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    status=LoginAttempt.Status.FAILED,
                    failure_reason='User not found'
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """Handle user logout by blacklisting refresh token."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user profile information."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UpdateProfileView(generics.UpdateAPIView):
    """Update user profile information."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChangePasswordView(APIView):
    """Handle password change for authenticated users."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.password_changed_at = timezone.now()
            user.save(update_fields=['password', 'password_changed_at'])
            
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Placeholder views for features not yet implemented
class VerifyEmailView(APIView):
    """Placeholder email verification view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Email verification endpoint - Coming soon'}, status=status.HTTP_200_OK)


class VerifyPhoneView(APIView):
    """Placeholder phone verification view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Phone verification endpoint - Coming soon'}, status=status.HTTP_200_OK)


class ResendVerificationView(APIView):
    """Placeholder resend verification view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Resend verification endpoint - Coming soon'}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """Placeholder password reset view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        return Response({'message': 'Password reset endpoint - Coming soon'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Placeholder password reset confirm view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        return Response({'message': 'Password reset confirm endpoint - Coming soon'}, status=status.HTTP_200_OK)


class AccountRecoveryView(APIView):
    """Placeholder account recovery view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        return Response({'message': 'Account recovery endpoint - Coming soon'}, status=status.HTTP_200_OK)


# Admin views (placeholders)
class AdminUserListView(generics.ListAPIView):
    """Placeholder admin user list view"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        return Response({'message': 'Admin user list endpoint - Coming soon'}, status=status.HTTP_200_OK)


class AdminUserDetailView(generics.RetrieveAPIView):
    """Placeholder admin user detail view"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, user_id):
        return Response({'message': f'Admin user detail endpoint for {user_id} - Coming soon'}, status=status.HTTP_200_OK)


class AdminSessionListView(generics.ListAPIView):
    """Placeholder admin session list view"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        return Response({'message': 'Admin session list endpoint - Coming soon'}, status=status.HTTP_200_OK)


class AdminLoginAttemptListView(generics.ListAPIView):
    """Placeholder admin login attempt list view"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        return Response({'message': 'Admin login attempt list endpoint - Coming soon'}, status=status.HTTP_200_OK)
