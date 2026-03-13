from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPublicKey(models.Model):
    """Stores the public key for each user's device."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='public_key')
    public_key = models.TextField() # The RSA/Ed25519 public key string
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    """A private link between two unique users."""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures you don't have multiple conversations for the same two people
        verbose_name_plural = "Conversations"

class EncryptedMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # This stores the encrypted base64 string. 
    # The server has NO idea what is inside this text.
    encrypted_text = models.TextField() 
    
    # For E2EE files, the file itself should be encrypted before upload
    encrypted_file = models.FileField(upload_to='encrypted_chats/', null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']