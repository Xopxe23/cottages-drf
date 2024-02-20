from django.contrib import admin

from chats.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "display_users")
    list_display_links = ("id",)

    def display_users(self, obj):
        return ', '.join([user.email for user in obj.users.all()])
    display_users.short_description = 'Users'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", 'chat')
    list_display_links = ("id", 'user')
