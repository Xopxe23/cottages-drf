from django.contrib import admin

from users.models import User


@admin.register(User)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone_number")
    list_display_links = ("email", "phone_number")
