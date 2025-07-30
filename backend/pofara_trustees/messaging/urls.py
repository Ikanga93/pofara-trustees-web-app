"""
URL configuration for messaging app.
"""

from django.urls import path, include
from . import views

app_name = 'messaging'

urlpatterns = [
    # Conversations
    path('conversations/', views.ConversationListCreateView.as_view(), name='conversation_list_create'),
    path('conversations/<uuid:conversation_id>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<uuid:conversation_id>/messages/', views.MessageListCreateView.as_view(), name='message_list_create'),
    path('conversations/<uuid:conversation_id>/participants/', views.ParticipantListView.as_view(), name='participant_list'),
    
    # Messages
    path('messages/<uuid:message_id>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<uuid:message_id>/read/', views.MarkMessageReadView.as_view(), name='mark_message_read'),
    
    # Attachments
    path('attachments/', views.AttachmentListCreateView.as_view(), name='attachment_list_create'),
    path('attachments/<uuid:attachment_id>/', views.AttachmentDetailView.as_view(), name='attachment_detail'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<uuid:notification_id>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('notifications/<uuid:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('notifications/preferences/', views.NotificationPreferencesView.as_view(), name='notification_preferences'),
    
    # Utility endpoints
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
    path('search/', views.MessageSearchView.as_view(), name='message_search'),
] 