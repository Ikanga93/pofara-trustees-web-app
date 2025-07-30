"""
Inspector management models for the Pofara Trustees platform.
Includes inspector profiles, certifications, availability, and verification system.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import uuid

User = get_user_model()


class Inspector(models.Model):
    """
    Inspector profile extending the User model with inspector-specific information.
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        IN_REVIEW = 'in_review', 'Under Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        SUSPENDED = 'suspended', 'Suspended'
        INACTIVE = 'inactive', 'Inactive'
    
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry Level (0-2 years)'
        JUNIOR = 'junior', 'Junior (2-5 years)'
        SENIOR = 'senior', 'Senior (5-10 years)'
        EXPERT = 'expert', 'Expert (10+ years)'
    
    # Primary relationships
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inspector_profile')
    
    # Inspector status and verification
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verification_level = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Verification level from 0 (unverified) to 5 (fully verified)"
    )
    
    # Professional information
    license_number = models.CharField(max_length=100, blank=True, help_text="Professional license number")
    license_expiry = models.DateField(blank=True, null=True)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    # Specializations and skills
    specializations = models.JSONField(
        default=list,
        blank=True,
        help_text="List of inspection specializations (construction, electrical, plumbing, etc.)"
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="List of technical skills and competencies"
    )
    languages_spoken = models.JSONField(
        default=list,
        blank=True,
        help_text="Languages the inspector can communicate in"
    )
    
    # Service areas and availability
    service_regions = models.JSONField(
        default=list,
        blank=True,
        help_text="Regions or cities where inspector provides services"
    )
    travel_radius_km = models.PositiveIntegerField(
        default=50,
        help_text="Maximum travel distance in kilometers"
    )
    available_weekdays = models.JSONField(
        default=list,
        blank=True,
        help_text="Available days of the week (0=Monday, 6=Sunday)"
    )
    available_hours_start = models.TimeField(default='09:00')
    available_hours_end = models.TimeField(default='17:00')
    
    # Rates and pricing
    base_hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Base hourly rate in local currency"
    )
    travel_rate_per_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        help_text="Travel cost per kilometer"
    )
    minimum_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Minimum charge for any inspection"
    )
    
    # Performance metrics
    total_inspections = models.PositiveIntegerField(default=0)
    completed_inspections = models.PositiveIntegerField(default=0)
    cancelled_inspections = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_ratings = models.PositiveIntegerField(default=0)
    
    # Availability and status
    is_available = models.BooleanField(default=True)
    is_accepting_new_projects = models.BooleanField(default=True)
    last_active = models.DateTimeField(auto_now=True)
    
    # Background check and verification documents
    background_check_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('passed', 'Passed'),
            ('failed', 'Failed'),
            ('expired', 'Expired'),
        ],
        default='pending'
    )
    background_check_date = models.DateTimeField(blank=True, null=True)
    background_check_expiry = models.DateTimeField(blank=True, null=True)
    
    # Profile and portfolio
    bio = models.TextField(max_length=1000, blank=True, help_text="Professional bio and experience summary")
    portfolio_images = models.JSONField(
        default=list,
        blank=True,
        help_text="List of portfolio image URLs"
    )
    
    # Banking and payment information
    bank_account_verified = models.BooleanField(default=False)
    payment_method_verified = models.BooleanField(default=False)
    
    # Administrative fields
    onboarding_completed = models.BooleanField(default=False)
    onboarding_completed_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_inspectors'
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspectors'
        verbose_name = 'Inspector'
        verbose_name_plural = 'Inspectors'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['verification_level']),
            models.Index(fields=['is_available']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Inspector: {self.user.get_full_name() or self.user.username}"
    
    @property
    def completion_rate(self):
        """Calculate project completion rate as percentage."""
        if self.total_inspections == 0:
            return 0
        return (self.completed_inspections / self.total_inspections) * 100
    
    @property
    def is_verified(self):
        """Check if inspector meets minimum verification requirements."""
        return (
            self.verification_level >= 3 and
            self.background_check_status == 'passed' and
            self.bank_account_verified and
            self.status == self.Status.APPROVED
        )
    
    def update_rating(self, new_rating):
        """Update average rating with new rating."""
        total_score = self.average_rating * self.total_ratings + new_rating
        self.total_ratings += 1
        self.average_rating = total_score / self.total_ratings
        self.save(update_fields=['average_rating', 'total_ratings'])


class InspectorCertification(models.Model):
    """
    Professional certifications and qualifications for inspectors.
    """
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        EXPIRED = 'expired', 'Expired'
        SUSPENDED = 'suspended', 'Suspended'
        REVOKED = 'revoked', 'Revoked'
    
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='certifications')
    
    # Certification details
    name = models.CharField(max_length=200, help_text="Certification name")
    issuing_organization = models.CharField(max_length=200)
    certification_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    # Documentation
    certificate_image = models.ImageField(upload_to='certifications/%Y/%m/', blank=True, null=True)
    description = models.TextField(blank=True, help_text="Description of what this certification covers")
    
    # Verification
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_certifications'
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspector_certifications'
        verbose_name = 'Inspector Certification'
        verbose_name_plural = 'Inspector Certifications'
        unique_together = ['inspector', 'name', 'issuing_organization']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['verified']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.inspector.user.get_full_name()}"
    
    @property
    def is_expired(self):
        """Check if certification is expired."""
        if not self.expiry_date:
            return False
        return timezone.now().date() > self.expiry_date


class InspectorRating(models.Model):
    """
    Ratings and reviews for inspectors from users.
    """
    
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='inspector_ratings')
    
    # Rating details
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall rating from 1 to 5 stars"
    )
    quality_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Quality of work rating"
    )
    punctuality_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Punctuality and reliability rating"
    )
    communication_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Communication skills rating"
    )
    
    # Review text
    review_title = models.CharField(max_length=200, blank=True)
    review_text = models.TextField(blank=True, help_text="Written review from the user")
    
    # Recommendations
    would_recommend = models.BooleanField(default=True)
    would_hire_again = models.BooleanField(default=True)
    
    # Moderation
    is_verified = models.BooleanField(default=False, help_text="Rating verified as legitimate")
    is_flagged = models.BooleanField(default=False, help_text="Rating flagged for review")
    moderation_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspector_ratings'
        verbose_name = 'Inspector Rating'
        verbose_name_plural = 'Inspector Ratings'
        unique_together = ['inspector', 'user', 'project']
        indexes = [
            models.Index(fields=['inspector', 'created_at']),
            models.Index(fields=['overall_rating']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"Rating for {self.inspector.user.get_full_name()} - {self.overall_rating}/5 stars"


class InspectorAvailability(models.Model):
    """
    Specific availability windows and booking calendar for inspectors.
    """
    
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BOOKED = 'booked', 'Booked'
        BLOCKED = 'blocked', 'Blocked'
        HOLIDAY = 'holiday', 'Holiday'
    
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='availability_windows')
    
    # Time window
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    
    # Booking information
    booked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='booked_inspector_slots'
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='inspector_availability_slots'
    )
    
    # Notes and details
    notes = models.TextField(blank=True, help_text="Additional notes about this time slot")
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.JSONField(
        default=dict,
        blank=True,
        help_text="Recurring pattern configuration"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspector_availability'
        verbose_name = 'Inspector Availability'
        verbose_name_plural = 'Inspector Availability'
        unique_together = ['inspector', 'date', 'start_time']
        indexes = [
            models.Index(fields=['inspector', 'date']),
            models.Index(fields=['status']),
            models.Index(fields=['date', 'start_time']),
        ]
    
    def __str__(self):
        return f"{self.inspector.user.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"


class InspectorDocument(models.Model):
    """
    Documents uploaded by inspectors for verification and portfolio.
    """
    
    class DocumentType(models.TextChoices):
        ID_DOCUMENT = 'id_document', 'ID Document'
        LICENSE = 'license', 'Professional License'
        CERTIFICATE = 'certificate', 'Certificate'
        INSURANCE = 'insurance', 'Insurance Policy'
        PORTFOLIO = 'portfolio', 'Portfolio Sample'
        REFERENCE = 'reference', 'Reference Letter'
        OTHER = 'other', 'Other'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        EXPIRED = 'expired', 'Expired'
    
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='documents')
    
    # Document details
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='inspector_documents/%Y/%m/')
    
    # Verification
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_inspector_documents'
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    
    # Expiry tracking
    expiry_date = models.DateField(blank=True, null=True)
    expiry_reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspector_documents'
        verbose_name = 'Inspector Document'
        verbose_name_plural = 'Inspector Documents'
        indexes = [
            models.Index(fields=['inspector', 'document_type']),
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.inspector.user.get_full_name()}"
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if not self.expiry_date:
            return False
        return timezone.now().date() > self.expiry_date
