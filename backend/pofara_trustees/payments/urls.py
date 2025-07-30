"""
URL configuration for payments app.
"""

from django.urls import path, include
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment methods
    path('methods/', views.PaymentMethodListCreateView.as_view(), name='payment_method_list_create'),
    path('methods/<uuid:method_id>/', views.PaymentMethodDetailView.as_view(), name='payment_method_detail'),
    path('methods/<uuid:method_id>/verify/', views.VerifyPaymentMethodView.as_view(), name='verify_payment_method'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<uuid:transaction_id>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/create/', views.CreateTransactionView.as_view(), name='create_transaction'),
    
    # Escrow
    path('escrow/', views.EscrowAccountListView.as_view(), name='escrow_account_list'),
    path('escrow/<uuid:account_id>/', views.EscrowAccountDetailView.as_view(), name='escrow_account_detail'),
    path('escrow/<uuid:account_id>/deposit/', views.EscrowDepositView.as_view(), name='escrow_deposit'),
    path('escrow/<uuid:account_id>/release/', views.EscrowReleaseView.as_view(), name='escrow_release'),
    
    # Invoices
    path('invoices/', views.InvoiceListCreateView.as_view(), name='invoice_list_create'),
    path('invoices/<uuid:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<uuid:invoice_id>/pay/', views.PayInvoiceView.as_view(), name='pay_invoice'),
    
    # Disputes
    path('disputes/', views.DisputeListCreateView.as_view(), name='dispute_list_create'),
    path('disputes/<uuid:dispute_id>/', views.DisputeDetailView.as_view(), name='dispute_detail'),
    
    # Reports
    path('reports/', views.FinancialReportListView.as_view(), name='financial_report_list'),
    path('reports/<uuid:report_id>/', views.FinancialReportDetailView.as_view(), name='financial_report_detail'),
    path('reports/generate/', views.GenerateReportView.as_view(), name='generate_report'),
    
    # Webhooks and callbacks
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    path('webhooks/paypal/', views.PayPalWebhookView.as_view(), name='paypal_webhook'),
] 