import uuid

from django.db import models

from users.models import User


class ChatManager(models.Manager):
    def create_chat(self, user1: User, user2: User):
        if user1 == user2:
            raise ValueError("User1 и User2 должны быть разными пользователями.")
        users = sorted([user1, user2], key=lambda user: user.id)
        existing_chat = self.filter(users=users[0]).filter(users=users[1]).first()
        if existing_chat:
            return existing_chat
        new_chat = self.create()
        new_chat.users.add(*users)
        return new_chat


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='chats', limit_choices_to={'is_active': True}, blank=True)
    last_message = models.OneToOneField('Message', on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='last_message_for_chat')

    objects = ChatManager()

    def __str__(self):
        usernames = ', '.join(user.first_name for user in self.users.all())
        return f"Chat {self.id} between {usernames}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.user.email} in Chat {self.chat.id}"
