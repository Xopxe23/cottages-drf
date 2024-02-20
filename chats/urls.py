from django.urls import path

from chats.views import ChatMessageListView, user_chat_list

urlpatterns = [
    path('', user_chat_list, name='user-chat-list'),
    path('<uuid:chat_id>/', ChatMessageListView.as_view(), name='user-chat-detail')
]
