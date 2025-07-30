"""
User management models for the Pofara Trustees platform.
Includes custom user model, profiles, and role-based access control.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import uuid


class User(AbstractUser):
    """
    Custom user model with role-based access control.
    Extends Django's AbstractUser with additional fields and functionality.
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        USER = 'user', 'Regular User'
        INSPECTOR = 'inspector', 'Inspector'
        SUPPORT = 'support', 'Support Staff'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'
        PENDING = 'pending', 'Pending Verification'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Enhanced contact information
    phone_number = PhoneNumberField(blank=True, null=True, help_text="Phone number with country code")
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    # Security and tracking
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(blank=True, null=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Terms and privacy
    terms_accepted = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(blank=True, null=True)
    privacy_policy_accepted = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    @property
    def is_account_locked(self):
        """Check if account is currently locked due to failed login attempts."""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False
    
    @property
    def is_verified(self):
        """Check if user has completed basic verification (email and phone)."""
        return self.email_verified and (self.phone_verified or not self.phone_number)
    
    def can_login(self):
        """Check if user is allowed to login."""
        return (
            self.is_active and 
            self.status == self.Status.ACTIVE and 
            not self.is_account_locked and
            self.terms_accepted
        )
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration after failed login attempts."""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    
    def unlock_account(self):
        """Unlock account and reset failed login attempts."""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['account_locked_until', 'failed_login_attempts'])


class UserProfile(models.Model):
    """
    Extended user profile with additional information and preferences.
    One-to-one relationship with User model.
    """
    
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', 'Prefer not to say'
    
    # Primary relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal information
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Brief personal description")
    
    # Location information
    country = models.CharField(max_length=100, blank=True, help_text="Country of residence")
    city = models.CharField(max_length=100, blank=True, help_text="City of residence")
    address = models.TextField(blank=True, help_text="Full address")
    postal_code = models.CharField(max_length=20, blank=True)
    
    # African diaspora specific information
    country_of_origin = models.CharField(max_length=100, blank=True, help_text="African country of origin")
    languages_spoken = models.JSONField(default=list, blank=True, help_text="List of languages spoken")
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = PhoneNumberField(blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    
    # Verification and KYC
    id_document_type = models.CharField(max_length=50, blank=True, help_text="Type of ID document")
    id_document_number = models.CharField(max_length=100, blank=True)
    id_document_image = models.ImageField(upload_to='documents/id/%Y/%m/', blank=True, null=True)
    kyc_status = models.CharField(
        max_length=30, 
        choices=[
            ('pending', 'Pending'),
            ('in_review', 'In Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('additional_info_required', 'Additional Information Required'),
        ],
        default='pending'
    )
    kyc_completed_at = models.DateTimeField(blank=True, null=True)
    kyc_notes = models.TextField(blank=True, help_text="Internal notes for KYC process")
    
    # Preferences
    notification_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="User notification preferences (email, SMS, push)"
    )
    timezone = models.CharField(max_length=50, default='UTC')
    language_preference = models.CharField(max_length=10, default='en')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['country_of_origin']),
            models.Index(fields=['kyc_status']),
        ]
    
    def __str__(self):
        return f"Profile for {self.user.get_full_name() or self.user.username}"
    
    @property
    def is_kyc_completed(self):
        """Check if KYC verification is completed."""
        return self.kyc_status == 'approved'
    
    @property
    def full_address(self):
        """Return formatted full address."""
        address_parts = [
            self.address,
            self.city,
            self.country,
            self.postal_code
        ]
        return ', '.join(filter(None, address_parts))


class UserSession(models.Model):
    """
    Track user sessions for security monitoring and analytics.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    location_info = models.JSONField(default=dict, blank=True)
    
    # Session tracking
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"Session for {self.user.username} from {self.ip_address}"
    
    @property
    def is_expired(self):
        """Check if session is expired."""
        return timezone.now() > self.expires_at


class LoginAttempt(models.Model):
    """
    Track login attempts for security monitoring and rate limiting.
    """
    
    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        BLOCKED = 'blocked', 'Blocked'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts', null=True, blank=True)
    email = models.EmailField(help_text="Email used in login attempt")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    failure_reason = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'login_attempts'
        verbose_name = 'Login Attempt'
        verbose_name_plural = 'Login Attempts'
        indexes = [
            models.Index(fields=['email', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Login attempt for {self.email} from {self.ip_address} - {self.get_status_display()}"
