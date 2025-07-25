
from rest_framework import serializers
from .models import CustomUser, Message, Conversation

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

# 2. Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

# 3. Conversation Serializer with nested messages and participants
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_usernames', 'created_at', 'messages']

    def get_participant_usernames(self, obj):
        return [user.username for user in obj.participants.all()]

    def validate(self, data):
        # Dummy validation to use ValidationError
        if not data.get('participants'):
            raise serializers.ValidationError("At least one participant is required.")
        return data
