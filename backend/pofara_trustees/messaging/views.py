"""Placeholder views for messaging app"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

class ConversationListCreateView(generics.ListCreateAPIView):
    def get(self, request): return Response({'message': 'Conversations'}, status=status.HTTP_200_OK)

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, conversation_id): return Response({'message': f'Conversation {conversation_id}'}, status=status.HTTP_200_OK)

class MessageListCreateView(generics.ListCreateAPIView):
    def get(self, request, conversation_id): return Response({'message': 'Messages'}, status=status.HTTP_200_OK)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, message_id): return Response({'message': f'Message {message_id}'}, status=status.HTTP_200_OK)

class ParticipantListView(generics.ListAPIView):
    def get(self, request, conversation_id): return Response({'message': 'Participants'}, status=status.HTTP_200_OK)

class MarkMessageReadView(APIView):
    def post(self, request, message_id): return Response({'message': 'Message marked as read'}, status=status.HTTP_200_OK)

class AttachmentListCreateView(generics.ListCreateAPIView):
    def get(self, request): return Response({'message': 'Attachments'}, status=status.HTTP_200_OK)

class AttachmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, attachment_id): return Response({'message': f'Attachment {attachment_id}'}, status=status.HTTP_200_OK)

class NotificationListView(generics.ListAPIView):
    def get(self, request): return Response({'message': 'Notifications'}, status=status.HTTP_200_OK)

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, notification_id): return Response({'message': f'Notification {notification_id}'}, status=status.HTTP_200_OK)

class MarkNotificationReadView(APIView):
    def post(self, request, notification_id): return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)

class NotificationPreferencesView(generics.RetrieveUpdateAPIView):
    def get(self, request): return Response({'message': 'Notification preferences'}, status=status.HTTP_200_OK)

class UnreadCountView(APIView):
    def get(self, request): return Response({'message': 'Unread count'}, status=status.HTTP_200_OK)

class MessageSearchView(APIView):
    def get(self, request): return Response({'message': 'Message search'}, status=status.HTTP_200_OK)
