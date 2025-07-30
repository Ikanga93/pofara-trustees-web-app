"""
Messaging and communication models for the Pofara Trustees platform.
Includes secure messaging, notifications, and real-time communication features.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

User = get_user_model()


class Conversation(models.Model):
    """
    Conversation container for messages between multiple participants.
    """
    
    class ConversationType(models.TextChoices):
        DIRECT = 'direct', 'Direct Message'
        GROUP = 'group', 'Group Chat'
        PROJECT = 'project', 'Project Discussion'
        SUPPORT = 'support', 'Support Ticket'
        ANNOUNCEMENT = 'announcement', 'Announcement'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'
        CLOSED = 'closed', 'Closed'
        SUSPENDED = 'suspended', 'Suspended'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_type = models.CharField(max_length=20, choices=ConversationType.choices, default=ConversationType.DIRECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    # Conversation details
    title = models.CharField(max_length=200, blank=True, help_text="Conversation title for group chats")
    description = models.TextField(blank=True, help_text="Conversation description")
    
    # Participants
    participants = models.ManyToManyField(
        User,
        through='ConversationParticipant',
        through_fields=('conversation', 'user'),
        related_name='conversations'
    )
    
    # Related objects (polymorphic relationship)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Settings
    is_encrypted = models.BooleanField(default=True, help_text="End-to-end encryption enabled")
    allow_file_sharing = models.BooleanField(default=True)
    auto_archive_days = models.PositiveIntegerField(default=0, help_text="Auto-archive after X days (0 = never)")
    
    # Creator and ownership
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_conversations')
    
    # Activity tracking
    last_message_at = models.DateTimeField(null=True, blank=True)
    message_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        indexes = [
            models.Index(fields=['conversation_type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['last_message_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]
        ordering = ['-last_message_at', '-created_at']
    
    def __str__(self):
        if self.title:
            return self.title
        participants = self.participants.all()[:3]
        participant_names = [p.get_full_name() or p.username for p in participants]
        if len(participants) > 3:
            participant_names.append(f"and {len(participants) - 3} others")
        return f"Conversation: {', '.join(participant_names)}"
    
    def add_participant(self, user, role='member', added_by=None):
        """Add a participant to the conversation."""
        participant, created = ConversationParticipant.objects.get_or_create(
            conversation=self,
            user=user,
            defaults={
                'role': role,
                'added_by': added_by or self.created_by,
                'joined_at': timezone.now()
            }
        )
        return participant
    
    def get_unread_count(self, user):
        """Get unread message count for a specific user."""
        try:
            participant = self.conversation_participants.get(user=user)
            return self.messages.filter(
                created_at__gt=participant.last_read_at or timezone.now()
            ).exclude(sender=user).count()
        except ConversationParticipant.DoesNotExist:
            return 0


class ConversationParticipant(models.Model):
    """
    Participant information for conversations with role-based permissions.
    """
    
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        MEMBER = 'member', 'Member'
        READ_ONLY = 'read_only', 'Read Only'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        LEFT = 'left', 'Left'
        REMOVED = 'removed', 'Removed'
        MUTED = 'muted', 'Muted'
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation_participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_participations')
    
    # Participant details
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    # Permissions
    can_send_messages = models.BooleanField(default=True)
    can_share_files = models.BooleanField(default=True)
    can_add_participants = models.BooleanField(default=False)
    can_remove_participants = models.BooleanField(default=False)
    
    # Activity tracking
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    last_active_at = models.DateTimeField(auto_now=True)
    
    # Management
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_participants'
    )
    
    # Notification preferences
    notifications_enabled = models.BooleanField(default=True)
    mention_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation_participants'
        verbose_name = 'Conversation Participant'
        verbose_name_plural = 'Conversation Participants'
        unique_together = ['conversation', 'user']
        indexes = [
            models.Index(fields=['conversation', 'status']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} in {self.conversation}"
    
    def mark_as_read(self):
        """Mark conversation as read for this participant."""
        self.last_read_at = timezone.now()
        self.save(update_fields=['last_read_at'])


class Message(models.Model):
    """
    Individual messages within conversations.
    """
    
    class MessageType(models.TextChoices):
        TEXT = 'text', 'Text Message'
        FILE = 'file', 'File Attachment'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        LOCATION = 'location', 'Location'
        SYSTEM = 'system', 'System Message'
        NOTIFICATION = 'notification', 'Notification'
    
    class Status(models.TextChoices):
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        READ = 'read', 'Read'
        FAILED = 'failed', 'Failed'
        DELETED = 'deleted', 'Deleted'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    # Message details
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=20, choices=MessageType.choices, default=MessageType.TEXT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SENT)
    
    # Content
    content = models.TextField(help_text="Message content (encrypted if encryption enabled)")
    plain_content = models.TextField(blank=True, help_text="Plain text content for search indexing")
    
    # Reply and threading
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )
    thread_root = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='thread_messages'
    )
    
    # Mentions and tags
    mentioned_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='mentioned_in_messages'
    )
    hashtags = models.JSONField(default=list, blank=True, help_text="Message hashtags")
    
    # File attachments
    attachments = models.JSONField(
        default=list,
        blank=True,
        help_text="List of file attachment metadata"
    )
    
    # Message metadata
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edit_history = models.JSONField(default=list, blank=True)
    
    # Encryption and security
    encryption_key_id = models.CharField(max_length=64, blank=True)
    signature = models.TextField(blank=True, help_text="Digital signature for message integrity")
    
    # Delivery tracking
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_by = models.ManyToManyField(
        User,
        through='MessageReadReceipt',
        related_name='read_messages'
    )
    
    # Priority and importance
    is_important = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    requires_response = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender']),
            models.Index(fields=['message_type']),
            models.Index(fields=['status']),
            models.Index(fields=['reply_to']),
            models.Index(fields=['is_important']),
        ]
        ordering = ['created_at']
    
    def __str__(self):
        content_preview = self.plain_content[:50] if self.plain_content else self.content[:50]
        return f"Message from {self.sender.get_full_name()}: {content_preview}..."
    
    def mark_as_read(self, user):
        """Mark message as read by a specific user."""
        receipt, created = MessageReadReceipt.objects.get_or_create(
            message=self,
            user=user,
            defaults={'read_at': timezone.now()}
        )
        return receipt


class MessageReadReceipt(models.Model):
    """
    Read receipts for tracking message delivery and read status.
    """
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_read_receipts')
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_read_receipts'
        verbose_name = 'Message Read Receipt'
        verbose_name_plural = 'Message Read Receipts'
        unique_together = ['message', 'user']
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['user', 'read_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} read message at {self.read_at}"


class MessageAttachment(models.Model):
    """
    File attachments for messages.
    """
    
    class AttachmentType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        DOCUMENT = 'document', 'Document'
        ARCHIVE = 'archive', 'Archive'
        OTHER = 'other', 'Other'
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_attachments')
    
    # File details
    file = models.FileField(upload_to='message_attachments/%Y/%m/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=50, help_text="MIME type")
    attachment_type = models.CharField(max_length=20, choices=AttachmentType.choices)
    
    # Preview and thumbnails
    thumbnail = models.ImageField(upload_to='message_thumbnails/%Y/%m/', blank=True, null=True)
    preview_url = models.URLField(blank=True, help_text="URL for file preview")
    
    # Security
    is_scanned = models.BooleanField(default=False, help_text="File scanned for malware")
    scan_result = models.CharField(max_length=50, blank=True)
    checksum = models.CharField(max_length=64, help_text="File integrity checksum")
    
    # Access control
    is_public = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_attachments'
        verbose_name = 'Message Attachment'
        verbose_name_plural = 'Message Attachments'
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['attachment_type']),
            models.Index(fields=['uploaded_at']),
        ]
    
    def __str__(self):
        return f"Attachment: {self.filename}"


class Notification(models.Model):
    """
    System notifications for users about various platform activities.
    """
    
    class NotificationType(models.TextChoices):
        MESSAGE = 'message', 'New Message'
        MENTION = 'mention', 'Mention'
        PROJECT_UPDATE = 'project_update', 'Project Update'
        MILESTONE_COMPLETED = 'milestone_completed', 'Milestone Completed'
        INSPECTION_SCHEDULED = 'inspection_scheduled', 'Inspection Scheduled'
        PAYMENT_RECEIVED = 'payment_received', 'Payment Received'
        PAYMENT_DUE = 'payment_due', 'Payment Due'
        VERIFICATION_REQUIRED = 'verification_required', 'Verification Required'
        SYSTEM_ALERT = 'system_alert', 'System Alert'
        WELCOME = 'welcome', 'Welcome'
        REMINDER = 'reminder', 'Reminder'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        NORMAL = 'normal', 'Normal'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SENT = 'sent', 'Sent'
        READ = 'read', 'Read'
        DISMISSED = 'dismissed', 'Dismissed'
        FAILED = 'failed', 'Failed'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification details
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    short_message = models.CharField(max_length=100, blank=True, help_text="Short version for mobile notifications")
    
    # Related object (polymorphic relationship)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Actions and links
    action_url = models.URLField(blank=True, help_text="URL to navigate to when notification is clicked")
    action_text = models.CharField(max_length=50, blank=True, help_text="Text for action button")
    
    # Delivery channels
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_push = models.BooleanField(default=True)
    send_in_app = models.BooleanField(default=True)
    
    # Scheduling
    scheduled_for = models.DateTimeField(null=True, blank=True, help_text="Schedule notification for future delivery")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Notification expiry time")
    
    # Delivery tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    sms_sent_at = models.DateTimeField(null=True, blank=True)
    push_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional notification metadata")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['scheduled_for']),
            models.Index(fields=['created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.get_full_name()}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if self.status != self.Status.READ:
            self.status = self.Status.READ
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])
    
    def is_expired(self):
        """Check if notification is expired."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class NotificationPreference(models.Model):
    """
    User preferences for different types of notifications.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Channel preferences
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    
    # Notification type preferences
    message_notifications = models.BooleanField(default=True)
    mention_notifications = models.BooleanField(default=True)
    project_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    system_notifications = models.BooleanField(default=True)
    
    # Timing preferences
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(default='22:00')
    quiet_hours_end = models.TimeField(default='08:00')
    
    # Frequency settings
    digest_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immediate'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('never', 'Never'),
        ],
        default='immediate'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Notification preferences for {self.user.get_full_name()}"
