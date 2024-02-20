from rest_framework import serializers

from chats.models import Chat, Message
from chats.services import get_chat_opponent
from users.serializers import UserFullNameSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']


class ChatListSerializer(serializers.ModelSerializer):
    opponent = UserFullNameSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'opponent', 'last_message']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get('user')
        opponent_user = get_chat_opponent(instance, user)
        representation['opponent'] = UserFullNameSerializer(opponent_user).data
        return representation
