"""
Payment and financial management models for the Pofara Trustees platform.
Includes payment processing, escrow services, invoices, and financial tracking.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid

User = get_user_model()


class PaymentMethod(models.Model):
    """
    User payment methods for processing payments.
    """
    
    class MethodType(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        DEBIT_CARD = 'debit_card', 'Debit Card'
        BANK_ACCOUNT = 'bank_account', 'Bank Account'
        DIGITAL_WALLET = 'digital_wallet', 'Digital Wallet'
        CRYPTOCURRENCY = 'cryptocurrency', 'Cryptocurrency'
        MOBILE_MONEY = 'mobile_money', 'Mobile Money'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING_VERIFICATION = 'pending_verification', 'Pending Verification'
        VERIFIED = 'verified', 'Verified'
        SUSPENDED = 'suspended', 'Suspended'
        EXPIRED = 'expired', 'Expired'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    
    # Method details
    method_type = models.CharField(max_length=20, choices=MethodType.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING_VERIFICATION)
    
    # Card/Account information (encrypted)
    masked_number = models.CharField(max_length=20, help_text="Masked card/account number for display")
    last_four_digits = models.CharField(max_length=4)
    brand = models.CharField(max_length=50, blank=True, help_text="Card brand or bank name")
    expiry_month = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    expiry_year = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(2020), MaxValueValidator(2050)])
    
    # Banking details
    bank_name = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=200, blank=True)
    routing_number = models.CharField(max_length=20, blank=True)
    swift_code = models.CharField(max_length=11, blank=True)
    
    # Address information
    billing_country = models.CharField(max_length=100, blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_address = models.TextField(blank=True)
    billing_postal_code = models.CharField(max_length=20, blank=True)
    
    # External provider information
    provider_id = models.CharField(max_length=100, blank=True, help_text="Payment provider identifier")
    provider_name = models.CharField(max_length=50, blank=True, help_text="Payment provider name")
    
    # Settings
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Security
    fingerprint = models.CharField(max_length=64, blank=True, help_text="Unique fingerprint for fraud detection")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_methods'
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['method_type']),
            models.Index(fields=['is_default']),
        ]
    
    def __str__(self):
        return f"{self.get_method_type_display()} ending in {self.last_four_digits}"


class Transaction(models.Model):
    """
    Financial transactions within the platform.
    """
    
    class TransactionType(models.TextChoices):
        PAYMENT = 'payment', 'Payment'
        REFUND = 'refund', 'Refund'
        PAYOUT = 'payout', 'Payout'
        ESCROW_DEPOSIT = 'escrow_deposit', 'Escrow Deposit'
        ESCROW_RELEASE = 'escrow_release', 'Escrow Release'
        FEE = 'fee', 'Platform Fee'
        BONUS = 'bonus', 'Bonus'
        PENALTY = 'penalty', 'Penalty'
        ADJUSTMENT = 'adjustment', 'Adjustment'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'
        DISPUTED = 'disputed', 'Disputed'
        REFUNDED = 'refunded', 'Refunded'
        PARTIALLY_REFUNDED = 'partially_refunded', 'Partially Refunded'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_number = models.CharField(max_length=50, unique=True, help_text="Unique transaction identifier")
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    
    # Parties involved
    payer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_made', null=True, blank=True)
    payee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_received', null=True, blank=True)
    
    # Financial details
    currency = models.CharField(max_length=3, default='USD', help_text="Currency code (ISO 4217)")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Transaction amount")
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Platform fee")
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Net amount after fees")
    
    # Exchange rate (for multi-currency)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000)
    original_currency = models.CharField(max_length=3, blank=True)
    original_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Payment method and provider
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    provider_name = models.CharField(max_length=50, blank=True)
    provider_transaction_id = models.CharField(max_length=100, blank=True)
    provider_reference = models.CharField(max_length=100, blank=True)
    
    # Related objects
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    milestone = models.ForeignKey(
        'projects.ProjectMilestone',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    invoice = models.ForeignKey(
        'Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    # Transaction details
    description = models.TextField(help_text="Transaction description")
    reference_number = models.CharField(max_length=100, blank=True, help_text="External reference number")
    
    # Processing details
    processed_at = models.DateTimeField(null=True, blank=True)
    authorized_at = models.DateTimeField(null=True, blank=True)
    captured_at = models.DateTimeField(null=True, blank=True)
    settled_at = models.DateTimeField(null=True, blank=True)
    
    # Failure information
    failure_code = models.CharField(max_length=50, blank=True)
    failure_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    # Security and compliance
    risk_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fraud risk score (0-100)"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional transaction metadata")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        indexes = [
            models.Index(fields=['transaction_number']),
            models.Index(fields=['payer', 'status']),
            models.Index(fields=['payee', 'status']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['status']),
            models.Index(fields=['project']),
            models.Index(fields=['created_at']),
            models.Index(fields=['processed_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_number}: {self.get_transaction_type_display()} - {self.amount} {self.currency}"


class EscrowAccount(models.Model):
    """
    Escrow accounts for holding funds during project execution.
    """
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FUNDED = 'funded', 'Funded'
        PARTIALLY_RELEASED = 'partially_released', 'Partially Released'
        FULLY_RELEASED = 'fully_released', 'Fully Released'
        DISPUTED = 'disputed', 'Disputed'
        REFUNDED = 'refunded', 'Refunded'
        CLOSED = 'closed', 'Closed'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=50, unique=True, help_text="Unique escrow account identifier")
    
    # Account details
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    
    # Parties
    depositor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='escrow_deposits')
    beneficiary = models.ForeignKey(User, on_delete=models.PROTECT, related_name='escrow_benefits')
    
    # Related project
    project = models.OneToOneField(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='escrow_account'
    )
    
    # Financial details
    currency = models.CharField(max_length=3, default='USD')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total escrow amount")
    available_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    reserved_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    released_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Terms and conditions
    terms = models.TextField(help_text="Escrow terms and conditions")
    release_conditions = models.JSONField(
        default=list,
        help_text="Conditions for fund release"
    )
    auto_release_enabled = models.BooleanField(default=False)
    auto_release_days = models.PositiveIntegerField(default=0)
    
    # Arbitration
    arbitrator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arbitrated_escrows'
    )
    dispute_deadline = models.DateField(null=True, blank=True)
    
    # Important dates
    funded_at = models.DateTimeField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'escrow_accounts'
        verbose_name = 'Escrow Account'
        verbose_name_plural = 'Escrow Accounts'
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['depositor']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['project']),
            models.Index(fields=['status']),
            models.Index(fields=['maturity_date']),
        ]
    
    def __str__(self):
        return f"Escrow {self.account_number} - {self.project.title}"
    
    @property
    def is_fully_funded(self):
        """Check if escrow is fully funded."""
        return self.available_balance >= self.total_amount
    
    @property
    def funding_percentage(self):
        """Calculate funding percentage."""
        if self.total_amount == 0:
            return 0
        return (self.available_balance / self.total_amount) * 100


class EscrowTransaction(models.Model):
    """
    Transactions related to escrow accounts (deposits, releases, etc.).
    """
    
    class TransactionType(models.TextChoices):
        DEPOSIT = 'deposit', 'Deposit'
        RELEASE = 'release', 'Release'
        REFUND = 'refund', 'Refund'
        DISPUTE_HOLD = 'dispute_hold', 'Dispute Hold'
        DISPUTE_RELEASE = 'dispute_release', 'Dispute Release'
        PENALTY = 'penalty', 'Penalty'
        INTEREST = 'interest', 'Interest'
    
    escrow_account = models.ForeignKey(EscrowAccount, on_delete=models.CASCADE, related_name='escrow_transactions')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='escrow_transaction')
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Release details (for releases)
    milestone = models.ForeignKey(
        'projects.ProjectMilestone',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escrow_releases'
    )
    release_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_escrow_releases'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Dispute information
    dispute = models.ForeignKey(
        'Dispute',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escrow_transactions'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'escrow_transactions'
        verbose_name = 'Escrow Transaction'
        verbose_name_plural = 'Escrow Transactions'
        indexes = [
            models.Index(fields=['escrow_account', 'transaction_type']),
            models.Index(fields=['transaction']),
            models.Index(fields=['milestone']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} {self.escrow_account.currency}"


class Invoice(models.Model):
    """
    Invoices for project payments and services.
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SENT = 'sent', 'Sent'
        VIEWED = 'viewed', 'Viewed'
        PAID = 'paid', 'Paid'
        OVERDUE = 'overdue', 'Overdue'
        DISPUTED = 'disputed', 'Disputed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'
    
    class InvoiceType(models.TextChoices):
        PROJECT_PAYMENT = 'project_payment', 'Project Payment'
        MILESTONE_PAYMENT = 'milestone_payment', 'Milestone Payment'
        INSPECTION_FEE = 'inspection_fee', 'Inspection Fee'
        PLATFORM_FEE = 'platform_fee', 'Platform Fee'
        PENALTY = 'penalty', 'Penalty'
        REFUND = 'refund', 'Refund'
        OTHER = 'other', 'Other'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=50, unique=True, help_text="Unique invoice identifier")
    
    # Invoice details
    invoice_type = models.CharField(max_length=30, choices=InvoiceType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Parties
    issued_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='issued_invoices')
    issued_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_invoices')
    
    # Related objects
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )
    milestone = models.ForeignKey(
        'projects.ProjectMilestone',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )
    
    # Financial details
    currency = models.CharField(max_length=3, default='USD')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Tax information
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    tax_number = models.CharField(max_length=50, blank=True, help_text="Tax registration number")
    
    # Invoice content
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    line_items = models.JSONField(default=list, help_text="Invoice line items")
    
    # Terms and conditions
    payment_terms = models.TextField(blank=True)
    due_date = models.DateField()
    late_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Notes and attachments
    notes = models.TextField(blank=True, help_text="Internal notes")
    public_notes = models.TextField(blank=True, help_text="Notes visible to customer")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['issued_by']),
            models.Index(fields=['issued_to']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['project']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.invoice_number}: {self.title}"
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        return (
            self.status not in [self.Status.PAID, self.Status.CANCELLED, self.Status.REFUNDED] and
            timezone.now().date() > self.due_date
        )
    
    @property
    def outstanding_amount(self):
        """Calculate outstanding amount."""
        return self.total_amount - self.paid_amount


class Dispute(models.Model):
    """
    Payment and transaction disputes.
    """
    
    class DisputeType(models.TextChoices):
        PAYMENT_DISPUTE = 'payment_dispute', 'Payment Dispute'
        SERVICE_DISPUTE = 'service_dispute', 'Service Dispute'
        QUALITY_DISPUTE = 'quality_dispute', 'Quality Dispute'
        REFUND_DISPUTE = 'refund_dispute', 'Refund Dispute'
        ESCROW_DISPUTE = 'escrow_dispute', 'Escrow Dispute'
        CHARGEBACK = 'chargeback', 'Chargeback'
        OTHER = 'other', 'Other'
    
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        UNDER_REVIEW = 'under_review', 'Under Review'
        AWAITING_RESPONSE = 'awaiting_response', 'Awaiting Response'
        MEDIATION = 'mediation', 'In Mediation'
        ARBITRATION = 'arbitration', 'In Arbitration'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    class Resolution(models.TextChoices):
        FAVOR_PLAINTIFF = 'favor_plaintiff', 'In Favor of Plaintiff'
        FAVOR_DEFENDANT = 'favor_defendant', 'In Favor of Defendant'
        PARTIAL_REFUND = 'partial_refund', 'Partial Refund'
        FULL_REFUND = 'full_refund', 'Full Refund'
        NO_ACTION = 'no_action', 'No Action Required'
        SETTLEMENT = 'settlement', 'Settlement Agreement'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispute_number = models.CharField(max_length=50, unique=True)
    
    # Dispute details
    dispute_type = models.CharField(max_length=30, choices=DisputeType.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN)
    
    # Parties
    plaintiff = models.ForeignKey(User, on_delete=models.PROTECT, related_name='initiated_disputes')
    defendant = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_disputes')
    mediator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mediated_disputes'
    )
    arbitrator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arbitrated_disputes'
    )
    
    # Related objects
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disputes'
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disputes'
    )
    
    # Dispute content
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of the dispute")
    disputed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Evidence
    evidence_documents = models.JSONField(default=list, blank=True)
    
    # Resolution
    resolution = models.CharField(max_length=30, choices=Resolution.choices, blank=True)
    resolution_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    
    # Important dates
    due_date = models.DateField(help_text="Response due date")
    escalated_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'disputes'
        verbose_name = 'Dispute'
        verbose_name_plural = 'Disputes'
        indexes = [
            models.Index(fields=['dispute_number']),
            models.Index(fields=['plaintiff']),
            models.Index(fields=['defendant']),
            models.Index(fields=['status']),
            models.Index(fields=['dispute_type']),
            models.Index(fields=['due_date']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.dispute_number}: {self.title}"


class FinancialReport(models.Model):
    """
    Financial reports and analytics for users and projects.
    """
    
    class ReportType(models.TextChoices):
        USER_STATEMENT = 'user_statement', 'User Statement'
        PROJECT_FINANCIALS = 'project_financials', 'Project Financials'
        TAX_REPORT = 'tax_report', 'Tax Report'
        ESCROW_SUMMARY = 'escrow_summary', 'Escrow Summary'
        TRANSACTION_SUMMARY = 'transaction_summary', 'Transaction Summary'
        REVENUE_REPORT = 'revenue_report', 'Revenue Report'
    
    class Status(models.TextChoices):
        GENERATING = 'generating', 'Generating'
        READY = 'ready', 'Ready'
        FAILED = 'failed', 'Failed'
        EXPIRED = 'expired', 'Expired'
    
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_number = models.CharField(max_length=50, unique=True)
    
    # Report details
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.GENERATING)
    
    # Scope
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_reports')
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='financial_reports'
    )
    
    # Report parameters
    period_start = models.DateField()
    period_end = models.DateField()
    currency = models.CharField(max_length=3, default='USD')
    
    # Report data
    data = models.JSONField(default=dict, help_text="Report data and calculations")
    summary = models.JSONField(default=dict, help_text="Report summary statistics")
    
    # File output
    file = models.FileField(upload_to='financial_reports/%Y/%m/', blank=True, null=True)
    file_format = models.CharField(max_length=10, default='pdf', help_text="Report file format")
    
    # Access control
    is_confidential = models.BooleanField(default=True)
    access_granted_to = models.ManyToManyField(
        User,
        blank=True,
        related_name='accessible_reports'
    )
    
    # Generation details
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_reports'
    )
    generated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'financial_reports'
        verbose_name = 'Financial Report'
        verbose_name_plural = 'Financial Reports'
        indexes = [
            models.Index(fields=['report_number']),
            models.Index(fields=['user', 'report_type']),
            models.Index(fields=['status']),
            models.Index(fields=['period_start', 'period_end']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.report_number}: {self.get_report_type_display()}"
