import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, EncryptedMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            
            # --- NEW: Sync offline messages ---
            await self.send_pending_messages()

    async def send_pending_messages(self):
        """Finds undelivered messages and pushes them to the newly connected user."""
        pending_messages = await self.get_pending_messages()
        for msg in pending_messages:
            await self.send(text_data=json.dumps({
                "type": "chat_message",
                "message": msg['encrypted_text'],
                "sender_id": msg['sender_id'],
                "conversation_id": msg['conversation_id'],
                "timestamp": str(msg['timestamp']),
                "is_sync": True # Tell Flutter this is an old message
            }))
            # Mark as delivered so they aren't sent again next time
            await self.mark_as_delivered(msg['id'])

    @database_sync_to_async
    def get_pending_messages(self):
        # Find messages in conversations this user is part of, 
        # which were NOT sent by this user and are NOT delivered yet.
        messages = EncryptedMessage.objects.filter(
            conversation__participants=self.user,
            is_delivered=False
        ).exclude(sender=self.user).values(
            'id', 'encrypted_text', 'sender_id', 'conversation_id', 'timestamp'
        )
        return list(messages)

    @database_sync_to_async
    def save_message(self, conv_id, text):
        try:
            # Check if conversation exists first
            if not Conversation.objects.filter(id=conv_id).exists():
                return None
                
            obj = EncryptedMessage.objects.create(
                conversation_id=conv_id,
                sender=self.user,
                encrypted_text=text
            )
            return obj.id
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    def mark_as_delivered(self, message_id):
        EncryptedMessage.objects.filter(id=message_id).update(is_delivered=True)

    async def receive(self, text_data):
        data = json.loads(text_data)
        recipient_id = data.get("recipient_id")
        encrypted_text = data.get("encrypted_text")
        conv_id = data.get("conversation_id")

        # Save to DB first
        msg_id = await self.save_message(conv_id, encrypted_text)
        
        if msg_id is None:
            await self.send(text_data=json.dumps({
                "error": "Invalid conversation_id or database error"
            }))
            return

        # Attempt to send to recipient's group
        await self.channel_layer.group_send(
            f"user_{recipient_id}",
            {
                "type": "chat_message",
                "message": encrypted_text,
                "sender_id": self.user.id,
                "conversation_id": conv_id,
                "db_id": msg_id # Include ID so recipient can acknowledge delivery
            }
        )

    async def chat_message(self, event):
        # Forward the event to the Flutter app
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, conv_id, text):
        obj = EncryptedMessage.objects.create(
            conversation_id=conv_id,
            sender=self.user,
            encrypted_text=text
        )
        return obj.id