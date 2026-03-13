from rest_framework import viewsets, status, permissions
from .models import Conversation, EncryptedMessage, UserPublicKey
from .serializers import EncryptedMessageSerializer, UserPublicKeySerializer

class PublicKeyViewSet(viewsets.ModelViewSet):
    queryset = UserPublicKey.objects.all()
    serializer_class = UserPublicKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        UserPublicKey.objects.update_or_create(
            user=self.request.user,
            defaults={'public_key': self.request.data.get('public_key')}
        )

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = EncryptedMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see messages from conversations they are part of
        return EncryptedMessage.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)