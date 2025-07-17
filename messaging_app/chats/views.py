from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations for the authenticated user.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return conversations where the current user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(participants=[request.user]) # Ensure the creator is a participant
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content'] # Assuming 'content' is the correct field name
    ordering_fields = ['timestamp'] # Assuming 'timestamp' is the correct field name
    ordering = ['-timestamp'] # Ordering by the most recent message first

    def get_queryset(self):
        """Return messages for a specific conversation."""
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, participants=self.request.user)
            return Message.objects.filter(conversation=conversation)
        return Message.objects.none() # Only show messages if a conversation ID is provided

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation_id = request.data.get('conversation')
        if not conversation_id:
            return Response({"error": "Conversation ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
