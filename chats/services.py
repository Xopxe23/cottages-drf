from django.db.models.query import QuerySet

from chats.models import Chat, Message
from users.models import User


def get_messages(chat: Chat) -> QuerySet[Message]:
    """Return messages from current chat."""
    return Message.objects.filter(chat=chat)


def get_chat_opponent(chat: Chat, current_user: User) -> User:
    """Get the opponent user in a chat."""
    try:
        opponent = chat.users.exclude(pk=current_user.pk).get()
        return opponent
    except User.DoesNotExist:
        raise User.DoesNotExist("Opponent user not found in the chat.")
    except User.MultipleObjectsReturned:
        raise User.MultipleObjectsReturned("Multiple users found in the chat, expected only one.")
