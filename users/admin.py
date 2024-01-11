from django.contrib import admin

from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone_number")
    list_display_links = ("email", "phone_number")


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")
