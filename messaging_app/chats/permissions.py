from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow owners of the object to access it
        return obj.user == request.user

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to only allow users to view messages or conversations
    where they are a participant.
    """

    def has_object_permission(self, request, view, obj):
        # For Message model: check sender or receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == request.user or obj.receiver == request.user

        # For Conversation model: check participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission: Only participants of a conversation can send, view, update, or delete messages.
    """

    def has_permission(self, request, view, obj):
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Message objects, check if the user is part of the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # For Conversation objects, check if the user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj, 'sender'):
            return obj.sender == request.user

        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
