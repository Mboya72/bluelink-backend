from rest_framework import serializers
from .models import Conversation, EncryptedMessage, UserPublicKey

class UserPublicKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPublicKey
        fields = ['user', 'public_key']

class EncryptedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptedMessage
        fields = ['id', 'conversation', 'sender', 'encrypted_text', 'encrypted_file', 'timestamp']
        read_only_fields = ['sender']

class ConversationSerializer(serializers.ModelSerializer):
    recipient_public_key = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'recipient_public_key']

    def get_recipient_public_key(self, obj):
        user = self.context['request'].user
        recipient = obj.participants.exclude(id=user.id).first()
        if recipient and hasattr(recipient, 'public_key'):
            return recipient.public_key.public_key
        return None