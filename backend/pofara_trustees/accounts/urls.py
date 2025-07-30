"""
URL configuration for accounts app.
Handles authentication, user registration, and profile management endpoints.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

app_name = 'accounts'

# JWT Authentication endpoints
auth_patterns = [
    path('token/', views.CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

# User management endpoints
user_patterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('verify-phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('resend-verification/', views.ResendVerificationView.as_view(), name='resend_verification'),
]

# Account recovery endpoints
recovery_patterns = [
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account-recovery/', views.AccountRecoveryView.as_view(), name='account_recovery'),
]

urlpatterns = [
    # Authentication
    path('', include(auth_patterns)),
    
    # User management
    path('user/', include(user_patterns)),
    
    # Account recovery
    path('recovery/', include(recovery_patterns)),
    
    # Admin and staff endpoints
    path('admin/users/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/<uuid:user_id>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/sessions/', views.AdminSessionListView.as_view(), name='admin_session_list'),
    path('admin/login-attempts/', views.AdminLoginAttemptListView.as_view(), name='admin_login_attempts'),
] 