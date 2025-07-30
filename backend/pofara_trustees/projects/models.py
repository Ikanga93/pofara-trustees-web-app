"""
Project management models for the Pofara Trustees platform.
Includes projects, milestones, updates, documents, and inspection reports.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid

User = get_user_model()


class Project(models.Model):
    """
    Main project model representing construction, business, or property management projects.
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        IN_PROGRESS = 'in_progress', 'In Progress'
        ON_HOLD = 'on_hold', 'On Hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        DISPUTED = 'disputed', 'Disputed'
    
    class ProjectType(models.TextChoices):
        CONSTRUCTION = 'construction', 'Construction'
        RENOVATION = 'renovation', 'Renovation'
        BUSINESS_SETUP = 'business_setup', 'Business Setup'
        PROPERTY_MANAGEMENT = 'property_management', 'Property Management'
        AGRICULTURE = 'agriculture', 'Agriculture'
        INVESTMENT = 'investment', 'Investment'
        OTHER = 'other', 'Other'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_number = models.CharField(max_length=20, unique=True, help_text="Unique project identifier")
    
    # Relationships
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    assigned_inspector = models.ForeignKey(
        'inspectors.Inspector',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_projects'
    )
    
    # Basic project information
    title = models.CharField(max_length=200, help_text="Project title")
    description = models.TextField(help_text="Detailed project description")
    project_type = models.CharField(max_length=30, choices=ProjectType.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    
    # Location information
    country = models.CharField(max_length=100, help_text="Country where project is located")
    state_province = models.CharField(max_length=100, blank=True, help_text="State or province")
    city = models.CharField(max_length=100, help_text="City")
    address = models.TextField(help_text="Full project address")
    postal_code = models.CharField(max_length=20, blank=True)
    coordinates_lat = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        help_text="Latitude coordinates"
    )
    coordinates_lng = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        help_text="Longitude coordinates"
    )
    
    # Financial information
    budget_currency = models.CharField(max_length=3, default='USD', help_text="Currency code (ISO 4217)")
    total_budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Total project budget"
    )
    spent_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="Amount already spent"
    )
    escrow_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="Amount held in escrow"
    )
    
    # Timeline information
    planned_start_date = models.DateField(help_text="Planned project start date")
    planned_end_date = models.DateField(help_text="Planned project completion date")
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    
    # Progress tracking
    completion_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Project completion percentage"
    )
    
    # Requirements and specifications
    requirements = models.JSONField(
        default=dict,
        blank=True,
        help_text="Project requirements and specifications"
    )
    deliverables = models.JSONField(
        default=list,
        blank=True,
        help_text="List of expected project deliverables"
    )
    
    # Communication and collaboration
    stakeholders = models.JSONField(
        default=list,
        blank=True,
        help_text="List of project stakeholders and their roles"
    )
    communication_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Communication preferences and frequency"
    )
    
    # Risk and compliance
    risk_assessment = models.TextField(blank=True, help_text="Risk assessment and mitigation strategies")
    compliance_requirements = models.JSONField(
        default=list,
        blank=True,
        help_text="Regulatory and compliance requirements"
    )
    
    # Quality and standards
    quality_standards = models.JSONField(
        default=list,
        blank=True,
        help_text="Quality standards and benchmarks"
    )
    success_criteria = models.TextField(blank=True, help_text="Project success criteria")
    
    # Settings and preferences
    is_public = models.BooleanField(default=False, help_text="Whether project is publicly visible")
    allow_inspector_applications = models.BooleanField(
        default=True,
        help_text="Allow inspectors to apply for this project"
    )
    requires_background_check = models.BooleanField(
        default=True,
        help_text="Require inspector background check"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['status']),
            models.Index(fields=['project_type']),
            models.Index(fields=['country', 'city']),
            models.Index(fields=['planned_start_date']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project_number}: {self.title}"
    
    @property
    def is_overdue(self):
        """Check if project is overdue."""
        if self.status == self.Status.COMPLETED:
            return False
        return timezone.now().date() > self.planned_end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining until planned end date."""
        if self.status == self.Status.COMPLETED:
            return 0
        delta = self.planned_end_date - timezone.now().date()
        return max(0, delta.days)
    
    @property
    def budget_remaining(self):
        """Calculate remaining budget."""
        return self.total_budget - self.spent_amount
    
    @property
    def budget_utilization_percentage(self):
        """Calculate budget utilization as percentage."""
        if self.total_budget == 0:
            return 0
        return (self.spent_amount / self.total_budget) * 100
    
    def update_completion_percentage(self):
        """Update completion percentage based on milestone progress."""
        milestones = self.milestones.all()
        if not milestones.exists():
            return
        
        completed_milestones = milestones.filter(status='completed').count()
        total_milestones = milestones.count()
        self.completion_percentage = (completed_milestones / total_milestones) * 100
        self.save(update_fields=['completion_percentage'])


class ProjectMilestone(models.Model):
    """
    Project milestones for tracking progress and payment releases.
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        OVERDUE = 'overdue', 'Overdue'
        CANCELLED = 'cancelled', 'Cancelled'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    
    # Milestone details
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(help_text="Milestone order in the project")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Timeline
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    
    # Financial
    budget_allocation = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Budget allocated to this milestone"
    )
    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Actual cost incurred"
    )
    payment_released = models.BooleanField(default=False)
    payment_release_date = models.DateTimeField(blank=True, null=True)
    
    # Requirements and deliverables
    deliverables = models.JSONField(
        default=list,
        blank=True,
        help_text="Specific deliverables for this milestone"
    )
    acceptance_criteria = models.TextField(
        blank=True,
        help_text="Criteria for milestone acceptance"
    )
    
    # Verification
    requires_inspection = models.BooleanField(default=True)
    inspection_completed = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_milestones'
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    
    # Progress tracking
    completion_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project_milestones'
        verbose_name = 'Project Milestone'
        verbose_name_plural = 'Project Milestones'
        unique_together = ['project', 'order']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['planned_end_date']),
            models.Index(fields=['status']),
        ]
        ordering = ['project', 'order']
    
    def __str__(self):
        return f"{self.project.project_number} - Milestone {self.order}: {self.title}"
    
    @property
    def is_overdue(self):
        """Check if milestone is overdue."""
        if self.status == self.Status.COMPLETED:
            return False
        return timezone.now().date() > self.planned_end_date


class ProjectUpdate(models.Model):
    """
    Regular updates and progress reports for projects.
    """
    
    class UpdateType(models.TextChoices):
        PROGRESS = 'progress', 'Progress Update'
        MILESTONE = 'milestone', 'Milestone Update'
        ISSUE = 'issue', 'Issue Report'
        FINANCIAL = 'financial', 'Financial Update'
        INSPECTION = 'inspection', 'Inspection Report'
        GENERAL = 'general', 'General Update'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    milestone = models.ForeignKey(
        ProjectMilestone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updates'
    )
    
    # Update details
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Update content and details")
    update_type = models.CharField(max_length=20, choices=UpdateType.choices, default=UpdateType.PROGRESS)
    
    # Author information
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updates')
    is_inspector_update = models.BooleanField(default=False)
    
    # Progress information
    progress_percentage = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Issues and concerns
    has_issues = models.BooleanField(default=False)
    issue_severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        blank=True
    )
    resolution_required = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    # Visibility and notifications
    is_public = models.BooleanField(default=True, help_text="Visible to project stakeholders")
    notify_stakeholders = models.BooleanField(default=True)
    notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project_updates'
        verbose_name = 'Project Update'
        verbose_name_plural = 'Project Updates'
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['update_type']),
            models.Index(fields=['has_issues']),
            models.Index(fields=['created_by']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.project_number} - {self.title}"


class ProjectDocument(models.Model):
    """
    Documents associated with projects (contracts, permits, reports, etc.).
    """
    
    class DocumentType(models.TextChoices):
        CONTRACT = 'contract', 'Contract'
        PERMIT = 'permit', 'Permit'
        BLUEPRINT = 'blueprint', 'Blueprint'
        SPECIFICATION = 'specification', 'Specification'
        INVOICE = 'invoice', 'Invoice'
        RECEIPT = 'receipt', 'Receipt'
        REPORT = 'report', 'Report'
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Video'
        OTHER = 'other', 'Other'
    
    class AccessLevel(models.TextChoices):
        PUBLIC = 'public', 'Public'
        STAKEHOLDERS = 'stakeholders', 'Stakeholders Only'
        OWNER_INSPECTOR = 'owner_inspector', 'Owner and Inspector Only'
        OWNER_ONLY = 'owner_only', 'Owner Only'
        CONFIDENTIAL = 'confidential', 'Confidential'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    milestone = models.ForeignKey(
        ProjectMilestone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    
    # Document details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    file = models.FileField(upload_to='project_documents/%Y/%m/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=50, help_text="MIME type")
    
    # Access and permissions
    access_level = models.CharField(max_length=20, choices=AccessLevel.choices, default=AccessLevel.STAKEHOLDERS)
    is_signed = models.BooleanField(default=False, help_text="Document is digitally signed")
    requires_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_documents'
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    
    # Version control
    version = models.CharField(max_length=20, default='1.0')
    is_latest_version = models.BooleanField(default=True)
    superseded_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supersedes'
    )
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    tags = models.JSONField(default=list, blank=True, help_text="Document tags for organization")
    checksum = models.CharField(max_length=64, blank=True, help_text="File integrity checksum")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project_documents'
        verbose_name = 'Project Document'
        verbose_name_plural = 'Project Documents'
        indexes = [
            models.Index(fields=['project', 'document_type']),
            models.Index(fields=['access_level']),
            models.Index(fields=['is_latest_version']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.project_number} - {self.title}"


class InspectionReport(models.Model):
    """
    Detailed inspection reports created by inspectors.
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        REVIEWED = 'reviewed', 'Reviewed'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    class OverallStatus(models.TextChoices):
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        SATISFACTORY = 'satisfactory', 'Satisfactory'
        NEEDS_IMPROVEMENT = 'needs_improvement', 'Needs Improvement'
        POOR = 'poor', 'Poor'
        FAILED = 'failed', 'Failed'
    
    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='inspection_reports')
    milestone = models.ForeignKey(
        ProjectMilestone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inspection_reports'
    )
    inspector = models.ForeignKey('inspectors.Inspector', on_delete=models.CASCADE, related_name='reports')
    
    # Report details
    report_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Executive summary of the inspection")
    detailed_findings = models.TextField(help_text="Detailed inspection findings")
    
    # Status and assessment
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    overall_status = models.CharField(max_length=30, choices=OverallStatus.choices)
    compliance_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Compliance score as percentage"
    )
    
    # Inspection details
    inspection_date = models.DateTimeField()
    inspection_duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Duration of inspection in hours"
    )
    weather_conditions = models.CharField(max_length=200, blank=True)
    access_conditions = models.CharField(max_length=200, blank=True)
    
    # Findings and recommendations
    issues_found = models.JSONField(
        default=list,
        blank=True,
        help_text="List of issues and problems found"
    )
    recommendations = models.JSONField(
        default=list,
        blank=True,
        help_text="List of recommendations for improvement"
    )
    next_inspection_date = models.DateField(blank=True, null=True)
    
    # Quality metrics
    safety_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Safety rating from 1 to 5"
    )
    quality_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Quality rating from 1 to 5"
    )
    progress_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Progress rating from 1 to 5"
    )
    
    # Approval and review
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports'
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    review_comments = models.TextField(blank=True)
    
    # Digital signature and verification
    inspector_signature = models.TextField(blank=True, help_text="Digital signature data")
    signature_timestamp = models.DateTimeField(blank=True, null=True)
    verification_hash = models.CharField(max_length=128, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inspection_reports'
        verbose_name = 'Inspection Report'
        verbose_name_plural = 'Inspection Reports'
        indexes = [
            models.Index(fields=['project', 'inspection_date']),
            models.Index(fields=['inspector', 'status']),
            models.Index(fields=['overall_status']),
            models.Index(fields=['compliance_score']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-inspection_date']
    
    def __str__(self):
        return f"{self.report_number}: {self.title}"


class ProjectComment(models.Model):
    """
    Comments and discussions on projects and reports.
    """
    
    class CommentType(models.TextChoices):
        GENERAL = 'general', 'General Comment'
        QUESTION = 'question', 'Question'
        CONCERN = 'concern', 'Concern'
        SUGGESTION = 'suggestion', 'Suggestion'
        APPROVAL = 'approval', 'Approval'
        REJECTION = 'rejection', 'Rejection'
    
    # Relationships - polymorphic to allow comments on different objects
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    milestone = models.ForeignKey(ProjectMilestone, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    update = models.ForeignKey(ProjectUpdate, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    
    # Comment details
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_comments')
    comment_type = models.CharField(max_length=20, choices=CommentType.choices, default=CommentType.GENERAL)
    content = models.TextField()
    
    # Threading for replies
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Status and moderation
    is_internal = models.BooleanField(default=False, help_text="Internal comment not visible to all stakeholders")
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_comments'
    )
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project_comments'
        verbose_name = 'Project Comment'
        verbose_name_plural = 'Project Comments'
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['comment_type']),
            models.Index(fields=['is_resolved']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        target = self.project or self.milestone or self.update or self.report
        return f"Comment by {self.author.get_full_name()} on {target}"
