"""
Django admin configuration for accounts app.
Provides comprehensive admin interface for user management.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from .models import User, UserProfile, UserSession, LoginAttempt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""
    
    list_display = [
        'username', 'email', 'get_full_name', 'role', 'status', 
        'is_verified', 'phone_verified', 'email_verified', 
        'is_active', 'date_joined'
    ]
    list_filter = [
        'role', 'status', 'is_active', 'email_verified', 
        'phone_verified', 'two_factor_enabled', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    readonly_fields = [
        'id', 'date_joined', 'last_login', 'password_changed_at',
        'created_at', 'updated_at', 'last_login_ip'
    ]
    ordering = ['-date_joined']
    
    # Fieldsets for add/edit forms
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Role & Status', {
            'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified', 'two_factor_enabled')
        }),
        ('Security', {
            'fields': ('failed_login_attempts', 'account_locked_until', 'last_login_ip'),
            'classes': ('collapse',)
        }),
        ('Terms & Privacy', {
            'fields': ('terms_accepted', 'terms_accepted_at', 'privacy_policy_accepted'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'password_changed_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Basic Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
    )
    
    actions = ['activate_users', 'deactivate_users', 'verify_email', 'unlock_accounts']
    
    def get_full_name(self, obj):
        """Display full name or username if no name provided."""
        return obj.get_full_name() or obj.username
    get_full_name.short_description = 'Full Name'
    
    def is_verified(self, obj):
        """Display verification status with colored indicator."""
        if obj.is_verified:
            return format_html(
                '<span style="color: green;">✓ Verified</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Not Verified</span>'
        )
    is_verified.short_description = 'Verified'
    
    def activate_users(self, request, queryset):
        """Bulk action to activate selected users."""
        count = queryset.update(status=User.Status.ACTIVE, is_active=True)
        self.message_user(request, f'{count} users have been activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        """Bulk action to deactivate selected users."""
        count = queryset.update(status=User.Status.INACTIVE, is_active=False)
        self.message_user(request, f'{count} users have been deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def verify_email(self, request, queryset):
        """Bulk action to verify email for selected users."""
        count = queryset.update(email_verified=True)
        self.message_user(request, f'Email verified for {count} users.')
    verify_email.short_description = 'Verify email for selected users'
    
    def unlock_accounts(self, request, queryset):
        """Bulk action to unlock selected user accounts."""
        count = 0
        for user in queryset:
            if user.is_account_locked:
                user.unlock_account()
                count += 1
        self.message_user(request, f'{count} user accounts have been unlocked.')
    unlock_accounts.short_description = 'Unlock selected accounts'


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    extra = 0
    readonly_fields = ['created_at', 'updated_at', 'kyc_completed_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('avatar', 'date_of_birth', 'gender', 'bio')
        }),
        ('Location', {
            'fields': ('country', 'city', 'address', 'postal_code')
        }),
        ('Diaspora Information', {
            'fields': ('country_of_origin', 'languages_spoken')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'),
            'classes': ('collapse',)
        }),
        ('KYC Verification', {
            'fields': ('id_document_type', 'id_document_number', 'id_document_image', 
                      'kyc_status', 'kyc_completed_at', 'kyc_notes'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('notification_preferences', 'timezone', 'language_preference'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    
    list_display = [
        'user', 'country', 'country_of_origin', 'kyc_status', 
        'is_kyc_completed', 'created_at'
    ]
    list_filter = ['kyc_status', 'country', 'country_of_origin', 'gender']
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'country', 'city', 'country_of_origin'
    ]
    readonly_fields = ['created_at', 'updated_at', 'kyc_completed_at']
    
    def is_kyc_completed(self, obj):
        """Display KYC completion status with colored indicator."""
        if obj.is_kyc_completed:
            return format_html(
                '<span style="color: green;">✓ Completed</span>'
            )
        return format_html(
            '<span style="color: orange;">Pending</span>'
        )
    is_kyc_completed.short_description = 'KYC Status'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin configuration for UserSession model."""
    
    list_display = [
        'user', 'ip_address', 'is_active', 'created_at', 'last_activity', 'expires_at'
    ]
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'ip_address', 'session_key']
    readonly_fields = ['created_at', 'last_activity']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """Disable adding sessions through admin."""
        return False
    
    actions = ['deactivate_sessions']
    
    def deactivate_sessions(self, request, queryset):
        """Bulk action to deactivate selected sessions."""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} sessions have been deactivated.')
    deactivate_sessions.short_description = 'Deactivate selected sessions'


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Admin configuration for LoginAttempt model."""
    
    list_display = [
        'email', 'user', 'ip_address', 'status', 'failure_reason', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['email', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """Disable adding login attempts through admin."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing login attempts through admin."""
        return False


# Add UserProfile inline to User admin
UserAdmin.inlines = [UserProfileInline]
