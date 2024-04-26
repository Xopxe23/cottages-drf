from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chats.models import Chat, Message
from chats.serializers import ChatListSerializer, MessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_chat_list(request) -> Response:
    user_chats = Chat.objects.filter(users=request.user.id).prefetch_related(
        'messages').select_related('last_message__user')
    serializer = ChatListSerializer(user_chats, many=True, context={'user': request.user})
    return Response(serializer.data)


class ChatMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[Message]:
        chat_id = self.kwargs.get('chat_id')
        get_object_or_404(Chat, pk=chat_id)
        queryset = Message.objects.filter(chat_id=chat_id).select_related('user').order_by('-timestamp')
        return queryset
