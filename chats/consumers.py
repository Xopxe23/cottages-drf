import json
from uuid import UUID

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chats.models import Chat, Message
from chats.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_group_name = None
        self.chat = None
        self.chat_id = None
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.chat = await self.get_chat()
        messages = await self.get_messages(self.chat_id)
        messages_serialized = await self.serialize_messages(messages)

        if not self.chat:
            await self.close()

        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(json.dumps(messages_serialized))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']

        await self.save_message(message_content)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat.message',
                'message': message_content
            }
        )

    async def chat_message(self, event):
        message_content = event['message']

        await self.send(text_data=json.dumps({
            'message': message_content
        }))

    @database_sync_to_async
    def save_message(self, message_content):
        Message.objects.create(chat=self.chat, user=self.user, content=message_content)

    @database_sync_to_async
    def get_chat(self):
        try:
            return Chat.objects.get(id=self.chat_id, users=self.user)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def get_messages(self, chat_id: UUID):
        return Message.objects.filter(chat=chat_id).order_by('-timestamp')[:2]

    @sync_to_async
    def serialize_messages(self, messages):
        return MessageSerializer(messages, many=True).data
