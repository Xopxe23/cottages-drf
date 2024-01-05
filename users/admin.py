from django.contrib import admin

from users.models import EmailUser


@admin.register(EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone_number")
    list_display_links = ("email", "phone_number")
