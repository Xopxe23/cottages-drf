from django.contrib import admin

from users.models import User, VerifyCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    list_display_links = ("email",)


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code")
    list_display_links = ("id", "user")
