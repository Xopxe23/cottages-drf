from django.contrib import admin

from relations.models import UserCottageLike, UserCottageRent, UserCottageReview


@admin.register(UserCottageReview)
class UserCottageReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "cottage", "user", "cottage_rating")
    list_display_links = ("id", "cottage", "user")


@admin.register(UserCottageLike)
class UserCottageLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "cottage", "user")
    list_display_links = ("id", "cottage", "user")


@admin.register(UserCottageRent)
class UserCottageRentAdmin(admin.ModelAdmin):
    list_display = ("id", "cottage", "user", "start_date", "end_date")
    list_display_links = ("id", "cottage", "user")